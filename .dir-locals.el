((nil . ((ispell-local-dictionary . "pt_BR,en_US")
         (org-export-headline-levels . 5)
         (org-latex-caption-above . (image src-block table special-block))
         (org-latex-prefer-user-labels . t)
         (org-latex-src-block-backend . minted)
         (org-ref-cite-insert-version . 2)))
 ("texto" . ((org-mode . ((bibtex-completion-bibliography . ("refs.bib"))
                           (bibtex-completion-additional-search-fields . ("peso"))
                           ;; A matriz de fontes, um arquivo por chave (ADR 0035),
                           ;; para o org-ref abrir pela citação. O caminho é
                           ;; absoluto: relativo, o bibtex-completion o procura de
                           ;; novo de dentro de fontes/ e escreve o modelo de notas
                           ;; por cima do arquivo que já existe.
                           (eval . (setq-local bibtex-completion-notes-path
                                               (expand-file-name
                                                "texto/fontes/"
                                                (locate-dominating-file
                                                 default-directory ".dir-locals.el"))))
                           ;; Só a chave: os campos do modelo saem no formato da
                           ;; APA ("Myers, Brad ({1994})"), e a referência curta
                           ;; se completa à mão.
                           (bibtex-completion-notes-template-multiple-files
                            . "#+title: ${=key=}: \n#+startup: overview\n\n")
                           (my/org-ref-glossary-files . ("../latex/siglas.tex"))
                           ;; Os capítulos na ordem do latex/tcc.tex, o
                           ;; tcc.tex e os apêndices: o rótulo de cada título
                           ;; sai do título (sec:delineamento), único no
                           ;; documento, e o ref: do org-ref lista e segue os
                           ;; rótulos de todos eles; o ref:chap:X abre o X.org.
                           ;; Arquivo fora da lista, como os de fontes/, fica
                           ;; com o rótulo sorteado do Org.
                           (gambi/org-document-files
                            . ("intro.org" "prog.org" "cases.org" "results.org"
                               "conclusion.org" "../latex/tcc.tex"
                               "../latex/apendices/*.tex")))))))
