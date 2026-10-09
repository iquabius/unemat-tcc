# A tela num módulo QML estático, que o aplicativo e o roteiro ligam.
qt_add_library(${CASO}-qml-tela STATIC)
qt_add_qml_module(${CASO}-qml-tela
  URI ListaFiltravel
  OUTPUT_DIRECTORY ListaFiltravel
  QML_FILES
    Main.qml
    estilo/Janela.qml estilo/Filtros.qml estilo/Rotulo.qml estilo/Entrada.qml
    estilo/Selecao.qml estilo/Contagem.qml estilo/Produtos.qml estilo/Produto.qml
  SOURCES ../dominio-cpp/DominioQml.h
)
target_include_directories(${CASO}-qml-tela PUBLIC ../dominio-cpp)
target_link_libraries(${CASO}-qml-tela PUBLIC ${CASO}-dominio-cpp Qt6::Quick Qt6::QuickControls2)

qt_add_executable(${CASO}-qml main.cpp)
target_link_libraries(${CASO}-qml PRIVATE ${CASO}-qml-tela ${CASO}-qml-telaplugin)
# O Qt do sistema é dinâmico: os módulos QML dele se carregam em tempo de
# execução, sem a busca de importações que um Qt estático pede.
set_target_properties(${CASO}-qml PROPERTIES QT_QML_MODULE_NO_IMPORT_SCAN TRUE)

qt_add_executable(${CASO}-qml-test test/RoteiroTest.cpp test/Tela.h)
target_link_libraries(${CASO}-qml-test PRIVATE ${CASO}-qml-tela ${CASO}-qml-telaplugin Qt6::Test)
set_target_properties(${CASO}-qml-test PROPERTIES QT_QML_MODULE_NO_IMPORT_SCAN TRUE)
add_test(NAME ${CASO}-qml COMMAND ${CASO}-qml-test)
set_tests_properties(${CASO}-qml PROPERTIES ENVIRONMENT QT_QPA_PLATFORM=offscreen)
