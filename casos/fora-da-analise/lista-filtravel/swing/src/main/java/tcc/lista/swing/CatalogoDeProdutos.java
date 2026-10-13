package tcc.lista.swing;

import static tcc.lista.DominioKt.comparador;
import static tcc.lista.DominioKt.correspondeABusca;
import static tcc.lista.DominioKt.daCategoria;
import static tcc.lista.DominioKt.formatarPreco;
import static tcc.lista.DominioKt.getCategorias;
import static tcc.lista.DominioKt.getProdutos;
import static tcc.lista.DominioKt.textoDaContagem;

import java.awt.BorderLayout;
import java.awt.Component;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import javax.swing.BoxLayout;
import javax.swing.DefaultListModel;
import javax.swing.JComboBox;
import javax.swing.JComponent;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.ListCellRenderer;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import tcc.lista.Ordem;
import tcc.lista.Produto;

// O catálogo em Swing, como o MainActivity do Views: os componentes ficam
// nesta classe, e cada listener refaz a lista inteira. (O getProdutos() e o
// getCategorias() são as propriedades produtos e categorias do domínio em
// Kotlin, vistas do Java.)
public class CatalogoDeProdutos extends JPanel {
    private final JTextField busca = new JTextField();
    private final JComboBox<String> categoria = new JComboBox<>(opcoesDeCategoria());
    private final JComboBox<String> ordem = new JComboBox<>(
            Arrays.stream(Ordem.values()).map(Ordem::getRotulo).toArray(String[]::new));
    private final JLabel contagem = new JLabel();
    // O modelo guarda os itens que a JList mostra, como o <ul> guarda os <li>.
    private final DefaultListModel<Produto> visiveis = new DefaultListModel<>();
    private final JList<Produto> lista = new JList<>(visiveis);
    private final JLabel vazio = new JLabel("Nenhum produto encontrado.");

    public CatalogoDeProdutos() {
        setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
        JPanel filtros = new JPanel();
        filtros.setLayout(new BoxLayout(filtros, BoxLayout.Y_AXIS));
        filtros.add(rotulo("Buscar", busca));
        filtros.add(rotulo("Categoria", categoria));
        filtros.add(rotulo("Ordenar por", ordem));
        add(filtros);
        add(contagem);
        add(new JScrollPane(lista));
        add(vazio);
        contagem.putClientProperty("classe", "contagem");
        vazio.putClientProperty("classe", "vazio");
        lista.setCellRenderer(new ItemDeProduto());

        // Como .on("input") e .on("change"): qualquer mudança refaz a lista.
        busca.getDocument().addDocumentListener(new DocumentListener() {
            @Override
            public void insertUpdate(DocumentEvent e) {
                atualizarLista();
            }

            @Override
            public void removeUpdate(DocumentEvent e) {
                atualizarLista();
            }

            @Override
            public void changedUpdate(DocumentEvent e) {
                atualizarLista();
            }
        });
        categoria.addActionListener(e -> atualizarLista());
        ordem.addActionListener(e -> atualizarLista());

        atualizarLista();
    }

    private static String[] opcoesDeCategoria() {
        List<String> opcoes = new ArrayList<>(List.of("Todas"));
        opcoes.addAll(getCategorias());
        return opcoes.toArray(String[]::new);
    }

    // Como o <label>: o texto e o controle que ele nomeia.
    private static JPanel rotulo(String texto, JComponent controle) {
        JLabel rotulo = new JLabel(texto);
        rotulo.setLabelFor(controle);
        JPanel painel = new JPanel();
        painel.setLayout(new BoxLayout(painel, BoxLayout.Y_AXIS));
        painel.add(rotulo);
        painel.add(controle);
        painel.putClientProperty("classe", "rotulo");
        return painel;
    }

    // Refaz a lista inteira a cada mudança num dos controles.
    private void atualizarLista() {
        String texto = busca.getText();
        int posicao = categoria.getSelectedIndex();
        String categoriaEscolhida = posicao == 0 ? "" : getCategorias().get(posicao - 1);
        Ordem ordemEscolhida = Ordem.values()[ordem.getSelectedIndex()];

        List<Produto> filtrados = getProdutos().stream()
                .filter(produto -> correspondeABusca(produto, texto) && daCategoria(produto, categoriaEscolhida))
                .sorted(comparador(ordemEscolhida))
                .toList();

        // Como o .empty().append(...): troca todos os itens de uma vez.
        visiveis.clear();
        visiveis.addAll(filtrados);
        contagem.setText(textoDaContagem(filtrados.size()));
        vazio.setVisible(filtrados.isEmpty());
    }

    // A JList não monta os itens: o renderer desenha cada produto com o mesmo
    // painel, preenchido de novo a cada item, no papel do map que monta os <li>.
    static class ItemDeProduto extends JPanel implements ListCellRenderer<Produto> {
        private final JLabel nome = new JLabel();
        private final JLabel categoria = new JLabel();
        private final JLabel preco = new JLabel();

        ItemDeProduto() {
            setLayout(new BorderLayout());
            JPanel textos = new JPanel();
            textos.setLayout(new BoxLayout(textos, BoxLayout.Y_AXIS));
            textos.add(nome);
            textos.add(categoria);
            add(textos, BorderLayout.CENTER);
            add(preco, BorderLayout.EAST);
            nome.putClientProperty("classe", "nome");
            categoria.putClientProperty("classe", "categoria");
            preco.putClientProperty("classe", "preco");
        }

        @Override
        public Component getListCellRendererComponent(
                JList<? extends Produto> lista, Produto produto, int posicao, boolean selecionado, boolean comFoco) {
            nome.setText(produto.getNome());
            categoria.setText(produto.getCategoria());
            preco.setText(formatarPreco(produto.getPreco()));
            return this;
        }
    }
}
