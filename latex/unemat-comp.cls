%% -------------------------------------------------------------------------
%% LaTeX document class for typesetting thesis
%% Ciência da Computação - Universidade do Estado de Mato Grosso
%%
%% Adapted from `inf-ufg.cls'
%% Instituto de Informática - Universidade Federal de Goiás
%% Author: Humberto Longo
%%
%% Any modified versions of this file must be renamed
%% with new filenames distinct from `unemat-comp.cls'
%%
%% -------------------------------------------------------------------------
%%
%% \CharacterTable
%%  {Upper-case    \A\B\C\D\E\F\G\H\I\J\K\L\M\N\O\P\Q\R\S\T\U\V\W\X\Y\Z
%%   Lower-case    \a\b\c\d\e\f\g\h\i\j\k\l\m\n\o\p\q\r\s\t\u\v\w\x\y\z
%%   Digits        \0\1\2\3\4\5\6\7\8\9
%%   Exclamation   \!     Double quote  \"     Hash (number) \#
%%   Dollar        \$     Percent       \%     Ampersand     \&
%%   Acute accent  \'     Left paren    \(     Right paren   \)
%%   Asterisk      \*     Plus          \+     Comma         \,
%%   Minus         \-     Point         \.     Solidus       \/
%%   Colon         \:     Semicolon     \;     Less than     \<
%%   Equals        \=     Greater than  \>     Question mark \?
%%   Commercial at \@     Left bracket  \[     Backslash     \\
%%   Right bracket \]     Circumflex    \^     Underscore    \_
%%   Grave accent  \`     Left brace    \{     Vertical bar  \|
%%   Right brace   \}     Tilde         \~}
%%
%% ----------------------------------------------------------------------------


%%======================================================================
%% unemat-comp Class Identification
%%======================================================================
\newcommand{\docdate}{}  % See the renewcommands below,
\newcommand{\filedate}{} % these contain the content;-))
\newcommand{\fileversion}{}
\renewcommand{\docdate}{2008/12/29}
\renewcommand{\filedate}{2008/12/29}
\renewcommand{\fileversion}{1.8}
\NeedsTeXFormat{LaTeX2e}[1999/12/01]
\ProvidesClass{tex/unemat-comp}%
[\filedate\space v\fileversion\space unemat-comp Thesis Class]
\typeout{LaTeX 2e package unemat-comp' -- Released 5 Aug 2017}

%%======================================================================
%% unemat-comp Class Options
%%======================================================================
\RequirePackage{ifthen}

\newboolean{tese} \setboolean{tese}{false}
\newboolean{diss} \setboolean{diss}{true}
\newboolean{mngr} \setboolean{mngr}{false}
\newboolean{rtcc} \setboolean{rtcc}{false}
\newboolean{abnt} \setboolean{abnt}{false}
\newboolean{link} \setboolean{link}{false}

\DeclareOption{tese}{
 \setboolean{tese}{true}
 \setboolean{diss}{false}
 \setboolean{mngr}{false}
 \setboolean{rtcc}{false}}

\DeclareOption{dissertacao}{
 \setboolean{tese}{false}
 \setboolean{diss}{true}
 \setboolean{mngr}{false}
 \setboolean{rtcc}{false}}

\DeclareOption{monografia}{
 \setboolean{tese}{false}
 \setboolean{diss}{false}
 \setboolean{mngr}{true}
 \setboolean{rtcc}{false}}

\DeclareOption{relatorio}{
 \setboolean{tese}{false}
 \setboolean{diss}{false}
 \setboolean{mngr}{false}
 \setboolean{rtcc}{true}}

\DeclareOption{abnt}{
 \setboolean{abnt}{true}}

\DeclareOption{nocolorlinks}{
 \setboolean{link}{true}}

\DeclareOption{american,english,french,german,brazil,portuguese}{
 \PassOptionsToPackage{\CurrentOption}{babel,fancyref}}

\ProcessOptions\relax

\def\titulo#1{\def\@titulo{#1}}                 \titulo{}
\def\subtitulo#1{\def\@subtitulo{#1}}           \subtitulo{}
\def\autor#1{\def\@autor{#1}}                   \autor{}
\def\autorR#1{\def\@autorR{#1}}                 \autorR{}
\def\orientador#1{\def\@orientador{#1}}         \orientador{}
\def\orientadora#1{\def\@orientadora{#1}}       \orientadora{}
\def\orientadorR#1{\def\@orientadorR{#1}}       \orientadorR{}
\def\orientadoraR#1{\def\@orientadoraR{#1}}     \orientadoraR{}
\def\coorientador#1{\def\@coorientador{#1}}     \coorientador{}
\def\coorientadora#1{\def\@coorientadora{#1}}   \coorientadora{}
\def\coorientadorR#1{\def\@coorientadorR{#1}}   \coorientadorR{}
\def\coorientadoraR#1{\def\@coorientadoraR{#1}} \coorientadoraR{}
\def\chaves#1{\def\@chaves{#1}}                 \chaves{}
\def\keys#1{\def\@keys{#1}}                     \keys{}
\def\dia#1{\def\@dia{#1}}                       \dia{}
\def\mes#1{\def\@mes{#1}}                       \mes{\month}
\def\@mesP{
  \ifcase\@mes\or
    Janeiro\or Fevereiro\or Mar\c{c}o\or
    Abril\or Maio\or Junho\or
    Julho\or Agosto\or Setembro\or
    Outubro\or Novembro\or Dezembro\fi}
\def\ano#1{\def\@ano{#1}}                       \ano{}
\def\cidade#1{\def\@cidade{#1}}                 \cidade{Goi\^ania}
\def\departamento#1{\def\@departamento{#1}}     \departamento{}
\def\unidadeco#1{\def\@unidadeco{#1}}           \unidadeco{Instituto de Inform\'atica}
\def\programa#1{\def\@programa{#1}}             \programa{Computa\c{c}\~ao}
\def\unidade#1{\def\@unidade{#1}}               \unidade{Instituto de Inform\'atica}
\def\universidade#1{\def\@universidade{#1}}     \universidade{Universidade Federal de Goi\'as}
\def\universidadeco#1{\def\@universidadeco{#1}} \universidadeco{Universidade Federal de Goi\'as}
\def\uni#1{\def\@uni{#1}}                       \uni{UFG}
\def\unico#1{\def\@unico{#1}}                   \unico{UFG}
\def\concentracao#1{\def\@concentracao{#1}}     \concentracao{Otimiza\c c\~ao}


%%======================================================================
%% unemat-comp Class Preliminary Declarations
%%======================================================================
\LoadClass[a4paper,12pt]{report}
\RequirePackage{texnames}

% Minhas alterações à Classe unemat-comp --- Comandos e Pacotes
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{amsfonts}

\RequirePackage{stmaryrd} % usei para obter o símbolo de subgrupo normal

\RequirePackage{graphicx}

\RequirePackage{pdfpages}


\usepackage{tikz}
\usetikzlibrary{matrix,arrows}

% \input{./meus-comandos/conectivos-e-quantificadores.sty}
% \input{./meus-comandos/conjuntos.sty}
% \input{./meus-comandos/funcoes.sty}
% \input{./meus-comandos/grupos.sty}

% Necessários para se acrescentar a Marca da Universidade na capa da Tese
\usepackage{blindtext,graphicx}
\usepackage[absolute]{textpos}
\usepackage{float}
\usepackage{longtable}

\setlength{\TPHorizModule}{1cm}
\setlength{\TPVertModule}{1cm}


% Hyphenation
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\RequirePackage[english,portuguese,brazil]{babel} % Termos pré-definidos em Português
\RequirePackage[utf8]{inputenc}                   % Inserção de acentos
\RequirePackage[T1]{fontenc}                      % Hifenização correta em Português

% Citations and References
% biblatex-abnt
\usepackage[
  % Biber já é a opção padrão no TeXLive 2016
  backend=biber,
  style=abnt,
  language=brazil,
  sortlocale=pt_BR,
  url=false,
  doi=true,
  eprint=false,
  maxcitenames=3,           % ABNT: até três autores, todos; quatro ou mais, et al.
  uniquelist=false,         % não desambigua "Autor; Coautor et al." entre obras do mesmo primeiro autor
  maxbibnames=100,
  uniquename=allinit,
  block        = space,   % Use spaces between blocks, making the text justified
  extradate,              % a letra de "2026a" também na referência (NBR 10520:2023)
  sortcites,              % várias obras numa chamada, na ordem da lista
  hyperref,               % Turn citations into links
]{biblatex}

% fornece o comando \textelp{} -> […]
\usepackage[autostyle]{csquotes}

%% Fontes adicionais
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
%\RequirePackage{amsfonts}
\RequirePackage{pslatex}
\newcommand{\arial}{\sf}

%% Verbatim
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\RequirePackage{fancyvrb}

%% Page layout
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\RequirePackage{indentfirst}
\RequirePackage{setspace}


% Escrita de ``Modelo'' na capa
% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\RequirePackage{eso-pic}
\newcommand{\modelo}{
 \AddToShipoutPicture*{%
  \setlength{\@tempdimb}{.5\paperwidth}%
  \setlength{\@tempdimc}{.5\paperheight}%
  \setlength{\unitlength}{1pt}%
  \put(\strip@pt\@tempdimb,\strip@pt\@tempdimc){%
  \makebox(-30,-30){\rotatebox{60}{\textcolor[gray]{0.90}%
  {\fontsize{8cm}{8cm}\selectfont{}}}}%
  }}}

% Referências cruzadas
% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\RequirePackage{lastpage}
\RequirePackage{ifpdf} % running on pdfTeX?
\ifpdf
 \RequirePackage[pdftex]{hyperref}
 \pdfadjustspacing=1    %%% force LaTeX-like character spacing
\else
 \RequirePackage[dvips,breaklinks]{hyperref}
\fi

\hypersetup{
 bookmarksopen=false,
 bookmarksnumbered=true,
 pdfstartview=FitH,
 hypertexnames=false,
 naturalnames=true,
}

\ifthenelse{\boolean{link}}
{}
{\hypersetup{
    % Texto em preto (NBR 14724, 5.1): os links continuam clicáveis, sem cor
    % nem retângulo.
    hidelinks,
    colorlinks=false,
    linkcolor=blue,             % Cor para links internos.
    citecolor=blue,             % Cor para citações referênciais no texto.
    urlcolor=blue,              % Cor para links URL da Internet.
    filecolor=blue,             % Cor para URLs que abrem arquivos locais.
    citebordercolor=0 1 0,      % Cor em RGB
    filebordercolor=0 .5 .5,
    linkbordercolor=1 0 0,
    urlbordercolor=0 1 1,
}}

% Siglas (ADR 0027): glossaries, depois do hyperref, ordenado pelo próprio
% TeX (\makenoidxglossaries), sem makeglossaries nem regra no latexmk.
% Sem hyperlink da sigla para a lista: no PDF, a sigla sai como texto comum.
\RequirePackage[acronym, nonumberlist, nopostdot, nogroupskip, toc=false,
  nohypertypes={acronym}]{glossaries}
\makenoidxglossaries
\setlength{\glsdescwidth}{.78\textwidth}
\newglossarystyle{siglas}{%
  \setglossarystyle{long}%
  \renewenvironment{theglossary}%
    {\begin{longtable}[l]{@{}p{.18\textwidth}p{\glsdescwidth}@{}}}%
    {\end{longtable}\addtocounter{table}{-1}}}% a longtable conta como tabela

% Figures
% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
%\ifpdf
% \RequirePackage[pdftex]{graphicx}
% \DeclareGraphicsExtensions{.jpg, .pdf, .mps, .png}
%\else
% \RequirePackage[dvips]{graphicx}
%\fi
%\RequirePackage[small,bf,up,format=hang,width=.75\textwidth]{caption}
%\renewcommand{\captionfont}{\small\itshape}
%\setlength{\abovecaptionskip}{0.5\abovecaptionskip}
%\setlength{\belowcaptionskip}{0.5\belowcaptionskip}

%% Subfigures
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\RequirePackage[IT,hang,FIGBOTCAP,TABBOTCAP]{subfigure}
\subfiglabelskip=3pt

%% algorithms
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\RequirePackage[ruled, algo2e, vlined, portuguese, algochapter]{algorithm2e}
\renewcommand{\listofalgorithmes}{\begingroup
 \tocfile{\listalgorithmcfname}{loa}
 \endgroup}

\usepackage{src_code}

% Legendas (NBR 14724:2024, 5.8 e 5.9): nome, número de ordem no texto,
% travessão e título, em espaço simples. A numeração é corrida, como nos
% modelos do curso, e não reinicia a cada seção primária.
\RequirePackage{caption}
% Referências separadas entre si por uma linha em branco de espaço simples
% (NBR 14724:2024, 5.2), e não de 1,5.
\AtBeginBibliography{\setlength{\bibitemsep}{14.5pt}}
% Hifenização de nomes que o padrão quebra errado.
\hyphenation{Type-Script Java-Script}

\captionsetup{labelsep=endash, font={stretch=1}, position=top}
\DeclareCaptionListFormat{figura}{\figurename~#2~--}
\DeclareCaptionListFormat{tabela}{\tablename~#2~--}
\DeclareCaptionListFormat{codigo}{\listingname~#2~--}
\captionsetup[figure]{listformat=figura}
\captionsetup[table]{listformat=tabela}
\captionsetup[listing]{listformat=codigo}
\counterwithout{figure}{chapter}
\counterwithout{table}{chapter}

%% Code lists
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
%\RequirePackage{float}
%\floatstyle{ruled}  %%% options: plain, boxed, ruled
%\newfloat{codigo}{htbp}{loc}[chapter] %% numera captions com número de seção.
%\floatname{codigo}{C\'{o}digo}
%\newcommand{\listofcodes}{
% \listof{codigo}{Lista de C\'{o}digos de Programas}
% \phantomsection
% \addcontentsline{toc}{chapter}{Lista de C\'{o}digos de Programas}}
% \newcommand{\listofcodes}{\begingroup
%  \tocfile{Lista de C\'{o}digos de Programas}{loc}
%  \endgroup}

%%======================================================================
%% Declarations
%%======================================================================

%% Page layout
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Margens de 3 cm em cima e à esquerda e de 2 cm embaixo e à direita, como os
% modelos do curso (w:pgMar 1701/1134), dentro do limite do regimento (Anexo
% II, item 5). O número da página fica a 2 cm da borda superior, como o
% cabeçalho dos modelos (w:header 1134). As notas \todo vão na margem
% esquerda, com 2,4 cm de largura, nas versões com e sem notas.
\RequirePackage[a4paper, left=3cm, right=2cm, top=3cm, bottom=2cm,
  headheight=14pt, headsep=0.64cm,
  marginparwidth=2.4cm, marginparsep=0.3cm]{geometry}
\setlength{\parindent}{1.5cm}
\addtolength{\skip\footins}{15pt}

%% line spacing
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\onehalfspacing
\frenchspacing
\clubpenalty=2000
\emergencystretch=20pt
\pretolerance=500
\tolerance=2500
\widowpenalty=2000

%% number of floats per page
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\renewcommand\floatpagefraction{.7}
\renewcommand\topfraction{.7}
\renewcommand\bottomfraction{.7}
\renewcommand\textfraction{.3}
\setcounter{totalnumber}{10}
\setcounter{topnumber}{10}
\setcounter{bottomnumber}{10}

%% Ambiente para citações diretas longas
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\newenvironment{citacao}%
  {\begin{spacing}{1.}%
   \small
   \begin{list}{}{%
       \setlength{\listparindent}{0cm}%
       \setlength{\itemindent}{\listparindent}%
       \setlength{\rightmargin}{0cm}%
       \setlength{\leftmargin}{\dimexpr4cm-\@totalleftmargin\relax}%
       \setlength{\parsep}{0pt}}%
    \item\relax}%
  {\end{list}\end{spacing}}
% O #+begin_quote do Org exporta quote: mesma forma da citação longa.
\renewenvironment{quote}{\begin{citacao}}{\end{citacao}}

%% Section titles
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% \def\mghrulefill#1{\leavevmode\leaders\hrule\@height #1\hfill\kern\z@}

% Seção primária (\chapter): no alto da mancha, à esquerda, 12 pt, negrito e
% caixa alta, o indicativo separado do título por um espaço e a segunda linha
% sob a primeira letra do título (regimento, Anexo II, XI; NBR 6024:2012);
% uma linha em branco de 1,5 antes do texto (NBR 14724:2024, 5.2).
\def\@makechapterhead#1{%
  {\parindent\z@ \raggedright \interlinepenalty\@M
   \normalfont\normalsize\bfseries
   \settowidth{\@tempdima}{\thechapter\space}%
   \hangindent\@tempdima \hangafter\@ne
   \thechapter\space\MakeUppercase{#1}\par\nobreak}%
  \vskip\baselineskip}

\def\@schapter#1{\if@twocolumn
                   \@topnewpage[\@makeschapterhead{#1}]%
                 \else
                   \@makeschapterhead{#1}%
                   \@afterheading
                 \fi}

% Títulos sem indicativo (sumário, listas, resumos, referências): centrados,
% com o destaque da seção primária (NBR 6024:2012).
\def\@makeschapterhead#1{%
  {\parindent\z@ \centering \interlinepenalty\@M
   \normalfont\normalsize\bfseries \MakeUppercase{#1}\par\nobreak}%
  \vskip\baselineskip}

% Destaque do regimento (Anexo II, XI) e do modelo
% Monografia_final_EXEMPLO.docx: secundária em negrito; da terciária em
% diante, negrito e itálico. Numeradas até a quinária, todas no sumário (NBR 6024 e 6027).
\usepackage{titlesec}
\setcounter{secnumdepth}{4}
\titleformat{\section}[hang]{\normalfont\normalsize\bfseries}{\thesection}{\wordsep}{}
\titleformat{\subsection}[hang]{\normalfont\normalsize\bfseries\itshape}{\thesubsection}{\wordsep}{}
\titleformat{\subsubsection}[hang]{\normalfont\normalsize\bfseries\itshape}{\thesubsubsection}{\wordsep}{}
\titleformat{\paragraph}[hang]{\normalfont\normalsize\bfseries\itshape}{\theparagraph}{\wordsep}{}
\titlespacing*{\section}{0pt}{\baselineskip}{\baselineskip}
\titlespacing*{\subsection}{0pt}{\baselineskip}{\baselineskip}
\titlespacing*{\subsubsection}{0pt}{\baselineskip}{\baselineskip}
\titlespacing*{\paragraph}{0pt}{\baselineskip}{\baselineskip}

%% header and footer
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\RequirePackage{fancyhdr}
\fancyhf{} % delete current setting for header and footer

\fancyhead[R]{\footnotesize \thepage}
\renewcommand{\headrulewidth}{0pt}

% As páginas pré-textuais são contadas, mas não numeradas (NBR 14724:2024,
% 5.3): o estilo plain, que o \chapter* do sumário e das listas usa, fica
% vazio até o \sumario, que liga o número a partir da Introdução.
\fancypagestyle{plain}{\fancyhf{}}
\newcommand{\@numerarpaginas}{%
  \fancypagestyle{plain}{\fancyhf{}\fancyhead[R]{\footnotesize\thepage}}%
  \pagestyle{fancy}}

% Remove o recuo do parágrafo nos rodapés
\usepackage[hang,flushmargin]{footmisc}

\RequirePackage{etoolbox}

% Apêndices: "APÊNDICE A – TÍTULO", centrado e com o destaque da seção
% primária, no texto e no sumário (NBR 14724:2024, 4.2.3.3).
\newcommand{\apendices}{%
  \cleardoublepage
  \appendix
  \def\@makechapterhead##1{%
    {\parindent\z@ \centering \interlinepenalty\@M
     \normalfont\normalsize\bfseries
     \MakeUppercase{\appendixname}\space\thechapter\space--\space\MakeUppercase{##1}\par\nobreak}%
    \vskip\baselineskip}%
  \addtocontents{toc}{%
    \protect\renewcommand*{\protect\cftchappresnum}{\protect\MakeUppercase{\appendixname}\space}%
    \protect\renewcommand*{\protect\cftchapaftersnum}{\space--}%
    \protect\settowidth{\protect\cftchapnumwidth}{\protect\bfseries\protect\MakeUppercase{\appendixname}\space M\space--\space}}%
}

\renewcommand\chapter{\if@openright\cleardoublepage\else\clearpage\fi
  \@mkboth{}{}
  \thispagestyle{plain}
  \global\@topnum\z@
  \@afterindentfalse
  \secdef\@capitulo\@schapter}

% A linha de cada seção primária no sumário sai em caixa alta, como o título
% no texto (NBR 6027:2012): o título curto, que vai para o sumário, chega ao
% \@chapter já em caixa alta; nos marcadores do PDF, como foi escrito.
% Cada seção primária define de novo as siglas na primeira ocorrência
% (\glsresetall), pela regra do AGENTS.md (ADR 0027).
\def\@capitulo[#1]#2{\glsresetall
  \@chapter[\texorpdfstring{\MakeUppercase{#1}}{#1}]{#2}}

%% table of contents
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Sumário (NBR 6027:2012): os indicativos alinhados à esquerda, os títulos
% alinhados pela margem do indicativo mais extenso e com o destaque que têm
% no texto. Os elementos pré-textuais ficam fora dele.
\RequirePackage[titles,subfigure]{tocloft}
\setcounter{tocdepth}{4}
\newlength{\@indicativo}
\settowidth{\@indicativo}{\normalsize\bfseries 0.0.0.0.0\space}
\renewcommand{\cftdotsep}{2}
\renewcommand{\cftchapleader}{\normalfont\cftdotfill{\cftdotsep}}
\renewcommand{\cftchappagefont}{\normalfont}
\setlength{\cftbeforechapskip}{0pt}
\renewcommand{\cftchapfont}{\bfseries}
\renewcommand{\cftsecfont}{\bfseries}
\renewcommand{\cftsubsecfont}{\bfseries\itshape}
\renewcommand{\cftsubsubsecfont}{\bfseries\itshape}
\renewcommand{\cftparafont}{\bfseries\itshape}
\cftsetindents{chapter}{0pt}{\@indicativo}
\cftsetindents{section}{0pt}{\@indicativo}
\cftsetindents{subsection}{0pt}{\@indicativo}
\cftsetindents{subsubsection}{0pt}{\@indicativo}
\cftsetindents{paragraph}{0pt}{\@indicativo}

% Listas de ilustrações e de tabelas (NBR 14724:2024, 4.2.1.9): cada linha
% com o nome, o número, o travessão e o título. O nome entra pelo listformat
% do caption, e a coluna cabe "Código 99 –".
\newlength{\@nomenalista}
\settowidth{\@nomenalista}{Código 99 --\space}
\cftsetindents{figure}{0pt}{\@nomenalista}
\cftsetindents{table}{0pt}{\@nomenalista}
\setlength{\cftbeforefigskip}{0pt}
\setlength{\cftbeforetabskip}{0pt}
% A lista de códigos (newfloat, do minted) usa o mesmo formato da de figuras.
\AtBeginDocument{\let\l@listing\l@figure}

%% theorems environments
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\renewcommand{\theequation}{\thechapter-\arabic{equation}}
\newtheorem{definition}{Defini\c{c}\~{a}o}[chapter]
\newtheorem{theorem}[definition]{Teorema}
\newtheorem{corollary}[definition]{Corol\'{a}rio}
\newtheorem{lemma}[definition]{Lema}
\newtheorem{proposition}[definition]{Proposi\c{c}\~{a}o}
\newtheorem{comment}[definition]{Observa\c{c}\~{a}o}
\newenvironment{proof}{\par \noindent \textit{Prova}.}{\hfill $\Box$\newline}

%% itemize environment
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\RequirePackage{enumitem}
% Listas como as alíneas da NBR 6024:2012 e de Garcia (2010): o marcador ou
% o rótulo recuado da margem, como o parágrafo, e a segunda linha do item
% sob a primeira letra do texto dele.
\setlist{noitemsep}
\setlist[itemize]{labelindent=\parindent, leftmargin=*}
\setlist[enumerate]{labelindent=\parindent, leftmargin=*}
\setlist[description]{labelindent=\parindent, leftmargin=\parindent,
  itemindent=0pt, labelwidth=0pt, labelsep=0.5em, style=standard}

\renewcommand{\cleardoublepage}{
 \clearpage\if@twoside \ifodd\c@page\else
 \thispagestyle{empty}
 \hbox{}\newpage\if@twocolumn\hbox{}\newpage\fi\fi\fi}
 
%%======================================================================
%% Pre-textual elements
%%======================================================================
\makeatletter

\newcommand{\margem}[1]{\hspace{0.5cm}\begin{minipage}[top]{13.0cm}#1\end{minipage}}
\newcommand{\textoC}[2]{\begin{center}\linespread{#1}#2\end{center}}
\newcommand{\textoF}[1]{\begin{minipage}[top]{12.0cm}#1\end{minipage}}
\newcommand{\textoD}[1]{\margem{\begin{flushright}#1\end{flushright}}}
\newcommand{\margemD}[1]{\hspace{3.5cm}\begin{minipage}[top]{10cm}#1\end{minipage}}

%% Capa
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Fonte de 12 pt em toda a capa (regimento, Anexo II, item 3); só os itens
% do Anexo II, I: instituição, autor, título, subtítulo, local e ano.
\newcommand{\capa}{%
 \ifpdf
  \pdfbookmark[0]{Elementos Pré-Textuais}{pretexto}
  \pdfbookmark[1]{Capa}{pretexto.1}
 \fi
 \hypersetup{
  pdftitle={\@titulo},
  pdfauthor={\@autor},
  pdfsubject={\@concentracao}
 }

 \modelo%
 \singlespacing%
 \begin{titlepage}%
   \begin{textblock}{5}(14.95,5.5)
     \includegraphics[height=3cm,width=2.8cm]{img/brasao/unemat_cor.png}
   \end{textblock}
   \begin{textblock}{5}(1.6,5.6)
     \includegraphics[height=2.5cm,width=2.73cm]{img/brasao/mt_cor.png}
   \end{textblock}
  \textoC{1}{\MakeUppercase{\@universidade}}%
  \vspace*{\stretch{-0.8}}%
  \textoC{1}{\MakeUppercase{Campus Universitário de \@cidade}}%
  \vspace*{\stretch{-0.8}}%
  \textoC{1}{\MakeUppercase{\@unidade}}%
  \ifthenelse{\equal{\@departamento}{}}{}{%
   \vspace*{\stretch{-0.8}}%
   \textoC{1}{\MakeUppercase{\@departamento}}}%
  \vspace*{\stretch{3}}%
  \textoC{1}{\MakeUppercase{\@autor}}%
  \vspace*{\stretch{4}}%
  \textoC{1}{\textbf{\MakeUppercase{\@titulo}}}%
  \ifthenelse{\equal{\@subtitulo}{}}{}{%
   \textoC{1}{\textbf{\MakeUppercase{\@subtitulo}}}}%
  \vspace*{\stretch{9}}%
  \textoC{1}{\MakeUppercase{\@cidade} \\ \@ano}%
 \end{titlepage}%
 \onehalfspacing%
 \normalfont%
}%


%% Autorização para publicação na Internet
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\newcommand{\publica}{\includepdf[pages={1},templatesize={250mm}{297mm}]{./pre/AutorizacaoPublicacao.pdf}}

%% Natureza do trabalho
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Tipo, objetivo, instituição e área de concentração, em espaço simples, do
% meio da mancha até a margem direita (NBR 14724:2024, 5.2), na folha de
% rosto e na de aprovação.
\newcommand{\@natureza}{%
 \par\hfill\begin{minipage}[t]{.5\textwidth}%
  \singlespacing\raggedright
  Trabalho de Conclus\~ao de Curso apresentado ao Curso de \@programa\ da
  \@unidade\ da \@universidade, como requisito parcial para obten\c c\~ao
  do t\'itulo de Bacharel em \@programa.%
  \ifthenelse{\equal{\@concentracao}{}}{}{%
   \par\medskip \'Area de concentra\c c\~ao: \@concentracao.}%
 \end{minipage}\par}

%% Folha de rosto
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Na ordem e na forma do regimento (Anexo II, II): autor em negrito e caixa
% alta no alto da mancha, a 3 cm da borda; título e subtítulo em negrito e
% caixa alta; natureza; orientador centrado; local em caixa alta e ano.
\newcommand{\rosto}{%
 \ifpdf
  \pdfbookmark[1]{Folha de Rosto}{pretexto.3}
 \fi
 \singlespacing%
 \textoC{1}{\textbf{\MakeUppercase{\@autor}}}%
 \vspace*{\stretch{3}}%
 \textoC{1}{\textbf{\MakeUppercase{\@titulo}}}%
 \ifthenelse{\equal{\@subtitulo}{}}{}{%
  \vspace*{1cm}%
  \textoC{1}{\textbf{\MakeUppercase{\@subtitulo}}}}%
 \vspace*{\stretch{3}}%
 \@natureza
 \vspace*{\stretch{1}}%
 \ifthenelse{\equal{\@orientador}{}}
  {\textoC{1}{Orientadora: Profa. \@orientadora}}%
  {\textoC{1}{Orientador: Prof. \@orientador}}%
 \ifthenelse{\equal{\@coorientador}{}}
  {\ifthenelse{\equal{\@coorientadora}{}}
   {}
   {\textoC{1}{Coorientadora: Profa. \@coorientadora}}}
  {\textoC{1}{Coorientador: Prof. \@coorientador}}%
 \vspace*{\stretch{6}}%
 \textoC{1}{\MakeUppercase{\@cidade} \\ \@ano}%
 \onehalfspacing%
 \normalfont%
 \clearpage%
}

%% Folha de aprovação
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Regimento, Art. 26 e Anexo II, III: título e subtítulo, local e data da
% aprovação, nome, assinatura e instituição de cada membro da banca. A banca
% vem de \examinadorUm e \examinadorDois no tcc.tex; sem nome, a linha
% fica para preencher.
\def\examinadorUm#1#2{\def\@examinadorUm{#1}\def\@instexaminadorUm{#2}}
\def\examinadorDois#1#2{\def\@examinadorDois{#1}\def\@instexaminadorDois{#2}}
\examinadorUm{}{}
\examinadorDois{}{}
\newcommand{\@assinatura}[3]{%
 \vspace*{\stretch{1}}%
 \textoC{1}{\rule{.7\textwidth}{0.5pt}\\
  \ifthenelse{\equal{#1}{}}{\phantom{Prof.}}{#1}\\
  \ifthenelse{\equal{#2}{}}{}{#2\\}%
  #3}}
\newcommand{\aprovacao}{%
 \ifpdf
  \pdfbookmark[1]{Folha de Aprovação}{pretexto.4}
 \fi
 \singlespacing%
 \textoC{1}{\textbf{\MakeUppercase{\@autor}}}%
 \vspace*{\stretch{1}}%
 \textoC{1}{\textbf{\MakeUppercase{\@titulo}}}%
 \ifthenelse{\equal{\@subtitulo}{}}{}{%
  \textoC{1}{\textbf{\MakeUppercase{\@subtitulo}}}}%
 \vspace*{\stretch{1}}%
 \@natureza
 \vspace*{\stretch{1}}%
 \textoC{1}{\@cidade, \rule{1cm}{0.5pt} de \rule{3cm}{0.5pt} de \rule{1.5cm}{0.5pt}.}%
 \vspace*{\stretch{1}}%
 \textoC{1}{\textbf{BANCA EXAMINADORA}}%
 \ifthenelse{\equal{\@orientador}{}}
  {\@assinatura{Profa. \@orientadora}{Orientadora e presidente da banca}{\@universidade}}
  {\@assinatura{Prof. \@orientador}{Orientador e presidente da banca}{\@universidade}}%
 \@assinatura{\@examinadorUm}{}{\@instexaminadorUm}%
 \@assinatura{\@examinadorDois}{}{\@instexaminadorDois}%
 \vspace*{\stretch{1}}%
 \onehalfspacing%
 \normalfont%
 \clearpage%
}

%% Direitos autorais
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\newcommand{\direitos}[1]{
 \ifpdf
  \pdfbookmark[1]{Direitos Autorais}{pretexto.5}
 \fi
 \singlespacing\arial%
 \margem{\normalfont \normalsize Todos os direitos reservados. \'{E} proibida
  a reprodu\c{c}\~{a}o total ou parcial do trabalho sem autoriza\c{c}\~{a}o da
  universidade, do autor e do orientador(a).}%
 \vspace*{\stretch{2}}%
 \par%
 \margem{\arial \textbf{\@autor}}%
 \vspace*{\stretch{0.2}}%
 \par%
 \margem{\normalfont #1}%
 \clearpage\onehalfspacing\normalfont%
}

%% dedicatoria
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\newenvironment{dedicatoria}{
 \ifpdf
  \pdfbookmark[1]{Dedicatória}{pretexto.6}
 \fi
 \normalfont\vspace*{\stretch{1}}
}{\clearpage}

%% Agradecimentos
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\newenvironment{agradecimentos}{
 \ifpdf
  \pdfbookmark[1]{Agradecimentos}{pretexto.7}
 \fi
 \@makeschapterhead{Agradecimentos}
}{\clearpage}

%% Resumo e abstract
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% NBR 6028:2021: parágrafo único e, logo abaixo, "Palavras-chave:" com os
% termos separados por ponto e vírgula e terminados por ponto, que o
% ambiente acrescenta. Espaço 1,5 (regimento, Anexo II, VII). Sem a
% referência do trabalho no topo, opcional quando o resumo está no próprio
% documento.
\newenvironment{resumo}{%
 \ifpdf
  \pdfbookmark[1]{Resumo}{pretexto.8}
 \fi
 \@makeschapterhead{Resumo}%
 \onehalfspacing\noindent\ignorespaces
}{%
 \par\vspace{\baselineskip}%
 \noindent Palavras-chave: \@chaves.%
 \clearpage
}

\renewenvironment{abstract}{%
 \ifpdf
  \pdfbookmark[1]{Abstract}{pretexto.9}
 \fi
 \begin{otherlanguage}{english}%
 \@makeschapterhead{Abstract}%
 \onehalfspacing\noindent\ignorespaces
}{%
 \par\vspace{\baselineskip}%
 \noindent Keywords: \@keys.%
 \end{otherlanguage}%
 \clearpage
}

%% Epígrafe
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
\newcommand{\epigrafe}[3]{%
  \ifpdf
   \pdfbookmark[1]{Epígrafe}{pretexto.10}
  \fi
  \thispagestyle{empty}\singlespacing\normalfont%
  \vspace*{\stretch{1}}\par%
  \begin{quotation}%
  #1%
  \par%
  \begin{flushright}
  \textbf{#2}, \\ \textit{#3}.
  \end{flushright}%
  \end{quotation}%
  \onehalfspacing
  \clearpage%
}

%% Sumário
%% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
%% The \IfSubStringInString command is based on H. Harders "substr" class.
%%
%% expands the first and second argument with
%% \protected@edef and calls #3 with them:
\newcommand\su@ExpandTwoArgs[3]{%
  \protected@edef\su@SubString{#1}%
  \protected@edef\su@String{#2}%
  \expandafter\expandafter\expandafter#3%
  \expandafter\expandafter\expandafter{%
    \expandafter\su@SubString\expandafter
  }\expandafter{\su@String}%
}
%%
%% tests if #1 in #2. If yes execute #3, else #4
\newcommand*\IfSubStringInString[2]{%
  \su@ExpandTwoArgs{#1}{#2}\su@IfSubStringInString
}
%%
\newcommand*\su@IfSubStringInString[2]{%
  \def\su@compare##1#1##2\@nil{%
    \def\su@param{##2}%
    \ifx\su@param\@empty
      \expandafter\@secondoftwo
    \else
      \expandafter\@firstoftwo
    \fi
  }%
  \su@compare#2#1\@nil
}
%%
% Listas de ilustrações (figuras, códigos, algoritmos) e de tabelas, nesta ordem e sem número de página
% (NBR 14724:2024, 4.2.1). Opções: fig, tab, alg e cod, em qualquer
% combinação. A lista de siglas vem depois, pelo \siglas, e o sumário por
% último, pelo \sumario.
\newcommand{\tabelas}[1][]
{
\begingroup\hypersetup{linkcolor=black}%
\singlespacing%
% Com a numeração corrida, sem o espaço que cada \chapter põe nas listas.
\renewcommand{\addvspace}[1]{}%
\IfSubStringInString{fig}{#1}
 {\listoffigures\clearpage
 }{}
\IfSubStringInString{cod}{#1}
 {\listoflistings\clearpage
 }{}
\IfSubStringInString{alg}{#1}
 {\listofalgorithmes\clearpage
 }{}
\IfSubStringInString{tab}{#1}
 {\listoftables\clearpage
 }{}
\endgroup
\onehalfspacing
}

% Lista de siglas: as siglas marcadas no texto com \gls, \glspl ou \acrshort
% (glossaries, entradas em latex/siglas.tex), em ordem alfabética.
\newcommand{\siglas}{%
 \begingroup\singlespacing
 \printnoidxglossary[type=\acronymtype, style=siglas, title={Lista de siglas}]%
 \endgroup
 \clearpage}

% Sumário, o último elemento pré-textual (NBR 6027:2012). Depois dele, a
% página passa a mostrar o número, e as siglas voltam a expandir na primeira
% ocorrência, caso o resumo tenha usado alguma.
\newcommand{\sumario}{%
 \ifpdf
  \pdfbookmark[0]{Sumário}{sumario}
 \fi
 \clearpage\singlespacing%
 {\hypersetup{linkcolor=black}\tableofcontents}%
 \clearpage%
 \normalfont\onehalfspacing
 \glsresetall
 \@numerarpaginas
}

\makeatother


%%======================================================================
%% unemat-comp Class Delayed Codes
%%======================================================================
\AtBeginDocument{%
  \author{\LARGE \arial \autor}%
  \title{\Huge \arial \titulo}%
  \date{\large \arial \data}%
  \pagestyle{empty}%
  }
\AtEndDocument{%
  \label{endpage}%
  }


%% Local Variables:
%% mode: LaTeX
%% End:
\endinput
%%======================================================================
%% End of file unemat-comp.cls'.
%%======================================================================
