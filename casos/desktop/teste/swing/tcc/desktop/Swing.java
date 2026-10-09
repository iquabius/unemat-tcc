package tcc.desktop;

import java.awt.Component;
import java.awt.Container;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Supplier;
import javax.swing.SwingUtilities;

// Apoio das Telas de teste do Swing, comum aos casos.
public final class Swing {
    private Swing() {}

    // Como a thread da interface do navegador: tudo roda na EDT do Swing, e
    // o teste espera o resultado.
    public static <T> T naTela(Supplier<T> bloco) {
        AtomicReference<T> resultado = new AtomicReference<>();
        try {
            SwingUtilities.invokeAndWait(() -> resultado.set(bloco.get()));
        } catch (InterruptedException | InvocationTargetException e) {
            throw new RuntimeException(e);
        }
        return resultado.get();
    }

    public static void naTela(Runnable bloco) {
        naTela(() -> {
            bloco.run();
            return null;
        });
    }

    // Todos os componentes abaixo de pai, de cima para baixo, como o
    // querySelectorAll.
    public static List<Component> componentes(Container pai) {
        List<Component> todos = new ArrayList<>();
        for (Component filho : pai.getComponents()) {
            todos.add(filho);
            if (filho instanceof Container container) {
                todos.addAll(componentes(container));
            }
        }
        return todos;
    }
}
