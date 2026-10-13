package tcc.formulario.javafx;

// Os campos de texto, pelo texto do rótulo que os nomeia.
enum Campo {
    NOME("Nome do passageiro"),
    EMAIL("E-mail"),
    IDA("Data de ida"),
    VOLTA("Data de volta");

    final String rotulo;

    Campo(String rotulo) {
        this.rotulo = rotulo;
    }
}
