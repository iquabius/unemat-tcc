#!/usr/bin/env python3
"""Confere o git commit do agente antes de ele rodar (hook PreToolUse).

O Claude Code chama este script antes de cada comando do Bash, pelo
.claude/settings.json, com o JSON do hook na entrada padrão. O git
commit do agente neste repositório, ou numa worktree dele, é recusado
quando:

- a skill commit-message não está no contexto da sessão (ou do subagente
  que commita): não foi carregada, ou foi antes da última compactação e
  a compactação não a reanexou;
- a mensagem, quando se lê do comando (-m, -F arquivo, -F - ou
  /dev/stdin com heredoc, -m "$(cat <<'EOF' ... EOF)"), quebra uma regra
  que se confere sem ler o diff:
  - a assinatura de ferramenta de IA no assunto ou no corpo (o emoji de
    robô; generated, created, made, written ou built com with, using ou
    by; gerado com com, pelo, por ou usando; criado com com ou usando;
    sempre antes do nome da ferramenta), e a linha de trailer cujo valor
    começa pelo nome dela com chave diferente de Co-Authored-By, no
    bloco de trailers ou colada ao corpo; a prosa que fala de IA não
    conta;
  - assunto com prefixo (tipo: ou [área]), começado por verbo em inglês,
    em minúscula, com ponto final (fora de abreviação, como et al.) ou
    com mais de 72 colunas (a junção de ramo, "Junta o ramo ...", fica
    livre da largura);
  - falta da linha em branco depois do assunto;
  - falta de corpo, salvo na junção de ramo; os trailers (chave com
    hífen, como Co-Authored-By, ou Refs, Fixes, Closes, Link e Cc) não
    contam como corpo;
  - linha do corpo com mais de 72 colunas, fora as sem espaço e as com
    URL;
- o commit é --fixup ou --squash no master ou no main, ou com o HEAD
  destacado na ponta de um deles (a worktree em que o merge se monta),
  lidos como estão antes do comando, sem contar um git checkout no mesmo
  comando.

O resto do eixo History da linus-review (uma mudança lógica por commit,
nada que um commit seguinte corrija, a mensagem que explica o porquê)
não se confere aqui: a recusa por falta da skill o lembra, e o AGENTS.md
o pede em cada commit.

Passam sem conferência:

- o commit de outro repositório (um de teste em /tmp, os dotfiles) e o
  de diretório que não se sabe (cd "$(mktemp -d)", GIT_DIR, --git-dir);
- o git merge, o git revert, o git cherry-pick e o git commit-tree: o
  revert, o cherry-pick e o commit-tree reaproveitam mensagens de
  commits que já existem e não fazem parte do processo de commit do
  agente;
- o git atrás de um prefixo que o parser não conhece (eval, xargs, sudo,
  nice, distrobox-host-exec, crase) ou dentro de um script gravado em
  arquivo;
- sem a conferência da mensagem, mas não sem a skill, o commit cuja
  mensagem o comando não deixa ler ao certo (variável sem valor
  conhecido; arquivo gravado por outro meio que não cat ou tee de um
  heredoc, ou citado por um comando anterior que não só o leia, como cp
  ou sed -i).

Para recusar, escreve a decisão na saída padrão; sem nada a dizer, sai
calado com 0. Entrada que não se lê também sai com 0: o hook não trava o
Bash por defeito próprio.
"""

import glob
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

LARGURA = 72
# O repositório cujos commits se conferem: o deste script.
REPOSITORIO = Path(__file__).resolve().parent.parent

# Corpo de heredoc (<<FIM, <<'FIM-CORPO', <<-FIM), trocado por um marcador
# antes de quebrar o comando em palavras; o resto da linha do << fica.
HEREDOC = re.compile(r"<<(-?)[ \t]*(['\"]?)([^\s'\"<>;&|()]+)\2([^\n]*)\n([\s\S]*?)"
                     r"^[ \t]*\3[ \t]*$", re.M)
MARCADOR = re.compile(r"<<H(\d+)$")
# A mensagem em -m "$(cat <<'EOF' ... EOF)", depois da troca do heredoc.
CAT_HEREDOC = re.compile(r"\$\(\s*cat\s+<<H(\d+)\s*\)$")

PONTUACAO = ";&|()\n"
# O que roda o comando seguinte, e os shells cujo -c se confere também.
PREFIXOS = {"command", "builtin", "exec", "nohup",
            "if", "then", "else", "elif", "do", "while", "until", "!", "{"}
SHELLS = {"sh", "bash", "dash", "zsh"}
# Opções globais do git que levam argumento na palavra seguinte.
GIT_COM_ARGUMENTO = {"-C", "-c", "--git-dir", "--work-tree", "--namespace",
                     "--config-env"}
# Opções curtas do git commit que levam argumento (na palavra seguinte ou
# colado); -u e -S só o aceitam colado.
COMMIT_COM_ARGUMENTO = set("mFCct")
COMMIT_LONGAS_COM_ARGUMENTO = {"--message", "--file", "--reuse-message",
                               "--reedit-message", "--fixup", "--squash",
                               "--template", "--author", "--date", "--cleanup",
                               "--trailer", "--pathspec-from-file"}

PREFIXO = re.compile(r"^(?:\[[^\]]+\]\s*|[a-z]+(?:\([^)]*\))?!?:\s)")
INGLES = {"add", "adds", "added", "fix", "fixes", "fixed", "update", "updates",
          "updated", "refactor", "implement", "rename", "change", "bump", "wip"}
# A assinatura que as ferramentas põem na mensagem ("Generated with
# [Claude Code]"); a prosa que fala de IA ("texto gerado por IA") não conta.
# O Cursor fica de fora: é o editor em que o autor revisa, e "o diff
# gerado pelo Cursor" é prosa.
FERRAMENTA_DE_IA = r"(?:claude|codex|copilot|chatgpt|gemini)\b"
# "Criado pelo Claude Code" é prosa sobre o que a ferramenta grava, e o
# criado só conta com com ou usando.
BANNER = re.compile(r"🤖|(?i:(?:\b(?:generated|created|made|written|built)\s+(?:with|using|by)"
                    r"|\bgerad[oa]\s+(?:com|pel[oa]|por|usando)|\bcriad[oa]\s+(?:com|usando))"
                    r"\s+\[?(?:o\s+)?" + FERRAMENTA_DE_IA + ")")
# Linha de trailer: chave com hífen (Co-Authored-By, Signed-off-by) ou uma
# das de uma palavra que o git usa; "Motivo: ..." é corpo.
CHAVE_DE_TRAILER = r"(?:[A-Za-z]+(?:-[A-Za-z]+)+|Refs?|Fixes|Closes|Link|Cc)"
TRAILER = re.compile(r"^" + CHAVE_DE_TRAILER + r": \S")
# Trailer cujo valor começa pelo nome de uma ferramenta de IA, com chave
# diferente de Co-Authored-By (Generated-By: Claude Code), no bloco de
# trailers ou colado ao corpo; "Refs: .claude/settings.json" não conta.
TRAILER_DE_IA = re.compile(r"(?i)^(?!co-authored-by:)" + CHAVE_DE_TRAILER
                           + r":\s*\[?" + FERRAMENTA_DE_IA)
# Caminhos do -F que leem a entrada padrão, como o -F -.
ENTRADA_PADRAO = {"-", "/dev/stdin", "/dev/fd/0", "/proc/self/fd/0"}
# Abreviação que pode fechar um assunto sem ser ponto final.
ABREVIACAO = re.compile(r"\b(?:al|etc|p|pp|v|cf)\.$")


def heredocs(cmd):
    """O comando com cada heredoc trocado por <<H<n>, e a lista dos corpos."""
    corpos = []

    def troca(m):
        corpo = m[5]
        if m[1]:
            corpo = re.sub(r"(?m)^\t+", "", corpo)
        corpos.append(corpo)
        return f"<<H{len(corpos) - 1}{m[4]}"

    return HEREDOC.sub(troca, cmd), corpos


def separador(palavra):
    return all(ch in PONTUACAO for ch in palavra)


def palavras(cmd):
    """As palavras do comando, com cada separador (; && | ( ) e a quebra
    de linha, sozinhos ou juntos, como "&&\\n") numa palavra própria; None
    se as aspas não fecham."""
    lex = shlex.shlex(cmd.replace("\\\n", " "), posix=True, punctuation_chars=PONTUACAO)
    lex.whitespace = " \t\r"
    lex.whitespace_split = True
    try:
        return list(lex)
    except ValueError:
        return None


def commits(cmd):
    """Cada git commit do comando, como dict: 'mensagens' (os -m), 'arquivo'
    (o -F), 'heredoc' (o corpo que o -F - lê), 'dir' (o diretório do
    commit relativo ao cwd do hook, pelos cd e pelo -C do git; None se não
    se sabe), 'reusa' (-C, -c, --no-edit...), 'fixup' (--fixup, --squash).
    O 'arquivo' sai com as variáveis atribuídas no comando já expandidas,
    ou com o $ quando cita uma que não se conhece."""
    cmd, corpos = heredocs(cmd)
    yield from commits_nas_palavras(palavras(cmd), corpos, ".", {}, {})


def expande(texto, vars_):
    """O texto com $VAR e ${VAR} trocados pelo valor atribuído no comando
    ou pelo do ambiente; None se sobra um $ que não se resolve."""
    def troca(m):
        nome = m[1] or m[2]
        valor = vars_[nome] if nome in vars_ else os.environ.get(nome)
        return m[0] if valor is None else valor

    texto = re.sub(r"\$(?:\{(\w+)\}|(\w+))", troca, texto)
    return None if "$" in texto else texto


def corpo_do_heredoc(corpos, m):
    n = int(m[1])
    return corpos[n] if n < len(corpos) else None


def commits_nas_palavras(ws, corpos, dir_, vars_, escritos):
    """Os commits nas palavras ws, seguindo os cd e as atribuições; o que
    muda dentro de ( ) ou $( ) deixa de valer depois do ). Em escritos
    ficam os arquivos que os comandos anteriores gravam ou citam (ver
    registra_escritas), que valem também depois do )."""
    if ws is None:
        return
    pilha = []
    i = 0
    while i < len(ws):
        if separador(ws[i]):
            for ch in ws[i]:
                if ch == "(":
                    pilha.append((dir_, dict(vars_)))
                elif ch == ")" and pilha:
                    dir_, vars_ = pilha.pop()
            i += 1
            continue
        j = pula_prefixos(ws, i)
        fim = j
        while fim < len(ws) and not separador(ws[fim]):
            fim += 1
        # a atribuição antes de um comando (VAR=x git ...) vale só para
        # ele; a solta e a do export ficam para os comandos seguintes
        vars_do_comando = dict(vars_) if j < fim and ws[i] != "export" else vars_
        for k in range(i, j):
            if re.match(r"^\w+=", ws[k]):
                nome, _, valor = ws[k].partition("=")
                vars_do_comando[nome] = expande(valor, vars_do_comando)
        nome = ws[j].rsplit("/", 1)[-1] if j < fim else ""
        # o env -C (ou --chdir) muda o diretório só do comando que roda
        dir_do_comando = dir_
        for k in range(i, j):
            if ws[k] in ("-C", "--chdir") and k + 1 < j:
                dir_do_comando = muda_dir(dir_do_comando, [ws[k + 1]], vars_do_comando)
            elif ws[k].startswith("--chdir="):
                dir_do_comando = muda_dir(dir_do_comando, [ws[k].split("=", 1)[1]],
                                          vars_do_comando)
        if nome != "git" or "commit" not in ws[j + 1:fim]:
            registra_escritas(ws[j:fim], corpos, dir_, vars_do_comando, escritos)
        if nome in ("cd", "pushd"):
            dir_ = muda_dir(dir_, ws[j + 1:fim], vars_do_comando)
        elif nome in SHELLS:
            texto = texto_do_c(ws[j + 1:fim])
            if texto is not None:
                yield from commits_nas_palavras(palavras(texto), corpos, dir_do_comando,
                                                dict(vars_do_comando), escritos)
        elif nome == "git":
            yield from commit_do_git(ws[j + 1:fim], corpos, dir_do_comando, vars_do_comando,
                                     escritos)
        i = fim


REDIRECIONAMENTO = re.compile(r"^\d*(>>?)\|?(.*)$")
# Comandos que só leem os arquivos que citam: mostrar a mensagem antes do
# commit (cat $M && git commit -F $M) não muda o que o commit lê.
SO_LEEM = {"cat", "head", "tail", "wc", "grep", "less", "diff", "file", "stat", "ls"}
GIT_SO_LE = {"add", "show", "diff", "log", "status"}


def chave_do_arquivo(palavra, dir_, vars_):
    """O caminho normalizado de palavra, relativo ao cwd do hook ou
    absoluto, para comparar arquivos; None se não se resolve."""
    p = caminho(expande(palavra, vars_))
    if p is None:
        return None
    if p.is_absolute():
        return os.path.normpath(p)
    return None if dir_ is None else os.path.normpath(os.path.join(dir_, p))


def registra_escritas(ws, corpos, dir_, vars_, escritos):
    """Guarda em escritos o que o comando ws faz a um arquivo antes do
    commit: o texto, quando é cat ou tee de um heredoc para ele (cat >
    $M <<'EOF'); None, quando o grava de outro jeito ou só o cita, e o
    que está no disco já não é o que o commit vai ler. O comando que só lê
    (SO_LEEM, e o git add, show, diff, log e status) não muda o arquivo
    que cita sem redirecionar para ele."""
    heredoc = None
    alvos = []
    k = 0
    while k < len(ws):
        m = MARCADOR.match(ws[k])
        r = REDIRECIONAMENTO.match(ws[k])
        if m:
            heredoc = corpo_do_heredoc(corpos, m)
        elif r:
            alvo = r[2]
            if not alvo and k + 1 < len(ws):
                k += 1
                alvo = ws[k]
            if alvo:
                alvos.append((alvo, r[1] == ">>"))
        k += 1
    nome = ws[0].rsplit("/", 1)[-1] if ws else ""
    if nome == "tee":
        alvos += [(a, "-a" in ws) for a in ws[1:] if not a.startswith("-")
                  and not MARCADOR.match(a) and not REDIRECIONAMENTO.match(a)]
    gravados = set()
    for alvo, acrescenta in alvos:
        chave = chave_do_arquivo(alvo, dir_, vars_)
        if chave is not None:
            gravados.add(chave)
            conhecido = nome in ("cat", "tee") and heredoc is not None and not acrescenta
            escritos[chave] = heredoc if conhecido else None
    if nome in SO_LEEM or (nome == "git" and len(ws) > 1 and ws[1] in GIT_SO_LE):
        return
    for palavra in ws[1:]:
        chave = chave_do_arquivo(palavra, dir_, vars_)
        if chave is not None and chave not in gravados:
            escritos[chave] = None


def pula_prefixos(ws, j):
    """O índice do comando, depois das atribuições (VAR=x), de command,
    exec, time, if, !, {..., do env com as opções e atribuições dele e do
    timeout com as opções e a duração."""
    while j < len(ws):
        if re.match(r"^\w+=", ws[j]) or ws[j] in PREFIXOS or ws[j] == "export":
            j += 1
        elif ws[j] == "env":
            j += 1
            while j < len(ws) and (ws[j].startswith("-") or re.match(r"^\w+=", ws[j])):
                j += 2 if ws[j] in ("-u", "-C", "-S", "--chdir", "--unset") else 1
        elif ws[j] == "time":
            j += 1
            while j < len(ws) and ws[j].startswith("-"):
                j += 1
        elif ws[j] == "timeout":
            j += 1
            while j < len(ws) and ws[j].startswith("-"):
                j += 2 if ws[j] in ("-s", "-k") else 1
            j += 1  # a duração
        else:
            return j
    # o timeout ou o env no fim do comando, sem o que eles rodariam
    return min(j, len(ws))


def muda_dir(dir_, args, vars_):
    """O diretório depois de cd args; None se não se sabe (cd -, cd sozinho,
    variável desconhecida, ou um diretório já desconhecido)."""
    args = [a for a in args if not a.startswith("-") or a == "-"]
    if dir_ is None or not args or args[0] == "-":
        return None
    destino = caminho(expande(args[0], vars_))
    return None if destino is None else str(Path(dir_, destino))


def caminho(texto):
    """O Path de texto com o ~ expandido; None se texto é None ou se o ~
    não se resolve (~usuario que não existe)."""
    if texto is None:
        return None
    try:
        return Path(texto).expanduser()
    except RuntimeError:
        return None


def texto_do_c(args):
    """O texto do -c de um shell (bash -lc 'texto'), ou None."""
    for k, a in enumerate(args):
        if re.match(r"^-\w*c\w*$", a):
            return args[k + 1] if k + 1 < len(args) else None
        if not a.startswith("-"):
            return None
    return None


def commit_do_git(args, corpos, dir_, vars_, escritos):
    """O commit de git args, se o subcomando é commit. O --git-dir, o
    --work-tree e o GIT_DIR apontam o commit para um repositório que o
    diretório não diz, e o deixam com 'dir' desconhecido."""
    if "GIT_DIR" in vars_ or "GIT_WORK_TREE" in vars_:
        dir_ = None
    k = 0
    while k < len(args) and args[k].startswith("-"):
        if args[k].split("=", 1)[0] in ("--git-dir", "--work-tree"):
            dir_ = None
        if args[k] in GIT_COM_ARGUMENTO and k + 1 < len(args):
            if args[k] == "-C":
                dir_ = muda_dir(dir_, [args[k + 1]], vars_)
            k += 2
        else:
            k += 1
    if k < len(args) and args[k] == "commit":
        c = opcoes_do_commit(args[k + 1:], corpos, vars_)
        c["dir"] = dir_
        if c["arquivo"] and c["arquivo"] not in ENTRADA_PADRAO:
            # sem valor conhecido, o $ fica, e a mensagem não se lê; o
            # commit segue no repositório e na exigência da skill
            c["arquivo"] = expande(c["arquivo"], vars_) or c["arquivo"]
            chave = chave_do_arquivo(c["arquivo"], dir_, vars_)
            if chave in escritos:
                c["arquivo"], c["heredoc"] = "-", escritos[chave]
        yield c


def opcoes_do_commit(args, corpos, vars_):
    """As opções que decidem a mensagem, lidas das palavras depois de
    commit; o marcador de heredoc conta também depois do --. O -m que cita
    variável sai expandido, ou None se ela não se resolve; o corpo do
    heredoc em "$(cat <<'EOF' ...)" é literal."""
    c = {"mensagens": [], "arquivo": None, "heredoc": None,
         "reusa": False, "fixup": False}

    def opcao(nome, arg):
        if nome in ("m", "--message"):
            m = CAT_HEREDOC.match(arg)
            c["mensagens"].append(corpo_do_heredoc(corpos, m) if m else expande(arg, vars_))
        elif nome in ("F", "--file"):
            c["arquivo"] = arg
        elif nome in ("C", "c", "--reuse-message", "--reedit-message"):
            c["reusa"] = True
        elif nome in ("--fixup", "--squash"):
            c["fixup"] = True

    caminhos = False
    j = 0
    while j < len(args):
        p = args[j]
        j += 1
        m = MARCADOR.match(p)
        if m:
            if c["arquivo"] in ENTRADA_PADRAO:
                c["heredoc"] = corpo_do_heredoc(corpos, m)
        elif caminhos:
            continue
        elif p == "--":
            caminhos = True
        elif p.startswith("--"):
            nome, igual, arg = p.partition("=")
            if nome == "--no-edit":
                c["reusa"] = True
            if nome in COMMIT_LONGAS_COM_ARGUMENTO:
                if not igual and j < len(args):
                    arg = args[j]
                    j += 1
                opcao(nome, arg)
        elif p.startswith("-") and len(p) > 1:
            for k, letra in enumerate(p[1:], 1):
                if letra in COMMIT_COM_ARGUMENTO:
                    arg = p[k + 1:]
                    if not arg and j < len(args):
                        arg = args[j]
                        j += 1
                    opcao(letra, arg)
                    break
                if letra in "uS":
                    break
    return c


def mensagem(c, cwd):
    """O texto da mensagem do commit, ou None se ele não se lê do comando."""
    if c["reusa"] and not c["mensagens"] and not c["arquivo"]:
        return None
    if c["mensagens"]:
        if None in c["mensagens"]:
            return None
        return "\n\n".join(m.strip("\n") for m in c["mensagens"])
    if c["arquivo"] in ENTRADA_PADRAO:
        return c["heredoc"]
    if c["arquivo"]:
        if "$" in c["arquivo"]:
            return None
        arquivo = caminho(c["arquivo"])
        if arquivo is None:
            return None
        if not arquivo.is_absolute():
            if c["dir"] is None:
                return None
            arquivo = Path(cwd, c["dir"], arquivo)
        try:
            return arquivo.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return None
    return None


def problemas_da_mensagem(texto):
    """As regras mecânicas que a mensagem quebra, uma frase por regra."""
    linhas = [l.rstrip() for l in texto.strip("\n").split("\n")]
    if not linhas or not linhas[0].strip():
        return ["a mensagem está vazia"]
    assunto = linhas[0]
    juncao = assunto.startswith("Junta o ramo ")
    # o bloco de trailers é o último parágrafo, se todas as linhas dele o são
    paragrafos, atual = [], []
    for l in linhas[2:]:
        if l.strip():
            atual.append(l)
        elif atual:
            paragrafos.append(atual)
            atual = []
    if atual:
        paragrafos.append(atual)
    trailers = paragrafos.pop() if paragrafos and all(TRAILER.match(l) for l in paragrafos[-1]) else []
    corpo = [l for p in paragrafos for l in p]

    problemas = []
    for l in [assunto] + corpo:
        if BANNER.search(l):
            problemas.append(f"banner de IA fora dos trailers: {l.strip()!r}; a "
                             "atribuição vai só no trailer Co-Authored-By")
    for l in corpo + trailers:
        if TRAILER_DE_IA.search(l):
            problemas.append(f"trailer de IA {l.split(':')[0]}: a atribuição vai só "
                             "no Co-Authored-By")
    if "co-authored-by" in assunto.lower():
        problemas.append("trailer no assunto")
    if PREFIXO.match(assunto):
        problemas.append(f"assunto com prefixo ({assunto.split(':')[0]}:); o "
                         "repositório não usa prefixo")
    primeira = assunto.split()[0].lower() if assunto.split() else ""
    if primeira in INGLES:
        problemas.append(f"assunto em inglês ({assunto.split()[0]}); a mensagem é em "
                         "português, no imperativo do repositório (Corrige, Junta...)")
    if assunto[:1].islower():
        problemas.append("assunto começa em minúscula")
    if assunto.endswith(".") and not ABREVIACAO.search(assunto):
        problemas.append("assunto termina em ponto")
    if not juncao and len(assunto) > LARGURA:
        problemas.append(f"assunto com {len(assunto)} colunas; o limite é {LARGURA}")
    if len(linhas) > 1 and linhas[1].strip():
        problemas.append("falta a linha em branco entre o assunto e o corpo")
    if not juncao and not corpo:
        problemas.append("sem corpo: todo commit do repositório diz o problema, o "
                         "porquê desta solução e como foi conferida")
    for l in corpo:
        if len(l) > LARGURA and " " in l.strip() and "://" not in l:
            problemas.append(f"linha do corpo com {len(l)} colunas (quebre em "
                             f"{LARGURA}): {l.strip()[:40]!r}...")
    return problemas


def eh_a_skill(nome):
    return nome == "commit-message" or str(nome).endswith(":commit-message")


def skill_carregada(dados):
    """True se a skill commit-message está no contexto: carregada desde a
    última compactação, ou reanexada por ela (o anexo invoked_skills que o
    Claude Code grava depois do compact_boundary). O transcript do
    subagente fica em <sessão>/subagents/, ou abaixo dali quando o
    subagente é de um workflow. None se o transcript não se lê, inclusive
    o do subagente que ainda não o tem."""
    caminho = dados.get("transcript_path")
    if not isinstance(caminho, str) or not caminho:
        return None
    caminho = Path(caminho)
    if dados.get("agent_id"):
        subagentes = caminho.with_suffix("") / "subagents"
        nome = f"agent-{dados['agent_id']}.jsonl"
        caminho = subagentes / nome
        if not caminho.exists():
            caminho = next(subagentes.rglob(glob.escape(nome)), caminho)
    try:
        linhas = caminho.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    carregada = False
    for linha in linhas:
        try:
            e = json.loads(linha)
        except ValueError:
            continue
        if not isinstance(e, dict):
            continue
        if e.get("type") == "system" and e.get("subtype") == "compact_boundary":
            carregada = False
            continue
        anexo = e.get("attachment")
        if (e.get("type") == "attachment" and isinstance(anexo, dict)
                and anexo.get("type") == "invoked_skills"):
            if any(isinstance(s, dict) and eh_a_skill(s.get("name"))
                   for s in anexo.get("skills") or []):
                carregada = True
            continue
        registro = e.get("message")
        conteudo = registro.get("content") if isinstance(registro, dict) else None
        if e.get("type") == "user":
            textos = [conteudo] if isinstance(conteudo, str) else [
                b.get("text") for b in conteudo if isinstance(b, dict)
                and b.get("type") == "text" and isinstance(b.get("text"), str)
            ] if isinstance(conteudo, list) else []
            if any("<command-name>/commit-message</command-name>" in t for t in textos):
                carregada = True
        elif e.get("type") == "assistant" and isinstance(conteudo, list):
            for b in conteudo:
                entrada = b.get("input") if isinstance(b, dict) else None
                if (isinstance(entrada, dict) and b.get("type") == "tool_use"
                        and b.get("name") == "Skill" and eh_a_skill(entrada.get("skill"))):
                    carregada = True
    return carregada


LEMBRETE = """\
Carregue a skill commit-message (ferramenta Skill) e reveja o commit pelos
critérios do eixo History da linus-review antes de commitar:
- uma mudança lógica por commit; mover, renomear ou reformatar vai num
  commit próprio, antes da mudança de lógica;
- nada que um commit seguinte corrija: o que corrige um commit do ramo
  entra nele, com --amend no último e --fixup=<sha> nos outros, que o
  ramo condensa antes do merge; commit novo só quando o conserto não
  corrige um commit só (AGENTS.md, "Código: ramo, revisão, merge");
- a mensagem diz o problema, o porquê desta solução e a alternativa
  recusada, e como foi conferida; não descreve o diff;
- sem banner de IA no assunto nem no corpo; a atribuição vai só no
  trailer Co-Authored-By.
Quando mostrar a mensagem e quando esperar o aprovo: AGENTS.md, seção
"Commits"."""


def git_saida(dir_, *args):
    """A saída de git -C dir_ args, ou None se ele falha."""
    try:
        r = subprocess.run(["git", "-C", str(dir_), *args], capture_output=True,
                           text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def git_comum(dir_):
    """O diretório git comum de dir_ (o mesmo para o checkout principal e
    as worktrees), ou None se dir_ não está num repositório."""
    comum = git_saida(dir_, "rev-parse", "--path-format=absolute", "--git-common-dir")
    return None if comum is None else Path(comum).resolve()


RAMOS_PRINCIPAIS = {"master", "main"}


def no_ramo_principal(dir_):
    """Se dir_ está no master ou no main, ou com o HEAD destacado na ponta
    de um deles (a worktree do passo 6 do merge). Lê o estado de antes do
    comando: um git checkout no mesmo comando não conta."""
    nome = git_saida(dir_, "symbolic-ref", "--quiet", "--short", "HEAD")
    if nome is not None:
        return nome in RAMOS_PRINCIPAIS
    cabeca = git_saida(dir_, "rev-parse", "--verify", "--quiet", "HEAD")
    return cabeca is not None and any(
        cabeca == git_saida(dir_, "rev-parse", "--verify", "--quiet", f"refs/heads/{r}")
        for r in RAMOS_PRINCIPAIS)


def neste_repositorio(c, cwd):
    """Se o commit c roda neste repositório; não, se o diretório dele não
    se sabe."""
    if c["dir"] is None:
        return False
    comum = git_comum(Path(cwd, c["dir"]))
    return comum is not None and comum == git_comum(REPOSITORIO)


def conferir(dados):
    """A razão da recusa, ou None se o comando passa."""
    entrada = dados.get("tool_input")
    if dados.get("tool_name") != "Bash" or not isinstance(entrada, dict):
        return None
    cmd = entrada.get("command")
    if not isinstance(cmd, str) or "commit" not in cmd:
        return None
    cwd = dados.get("cwd") if isinstance(dados.get("cwd"), str) else os.getcwd()
    cs = [c for c in commits(cmd) if neste_repositorio(c, cwd)]
    if not cs:
        return None
    problemas = []
    for c in cs:
        if c["fixup"] and no_ramo_principal(Path(cwd, c["dir"])):
            problemas.append("git commit --fixup/--squash no ramo principal: o "
                             "fixup! só existe para o rebase --autosquash que "
                             "condensa um ramo antes do merge; faça o conserto "
                             "num ramo próprio")
        texto = mensagem(c, cwd)
        if texto is not None:
            problemas += problemas_da_mensagem(texto)
    problemas = list(dict.fromkeys(problemas))
    sem_skill = skill_carregada(dados) is False
    if not problemas and not sem_skill:
        return None
    partes = ["Commit recusado pela conferência do repositório (bin/conferir-commit.py)."]
    if problemas:
        partes.append("Mensagem:\n" + "\n".join(f"- {p}" for p in problemas))
    if sem_skill:
        partes.append("A skill commit-message não foi carregada nesta sessão "
                      "(ou desde a última compactação).\n" + LEMBRETE)
    return "\n\n".join(partes)


def main():
    try:
        dados = json.load(sys.stdin)
    except ValueError:
        return 0
    if not isinstance(dados, dict):
        return 0
    razao = conferir(dados)
    if razao:
        json.dump({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": razao}}, sys.stdout, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
