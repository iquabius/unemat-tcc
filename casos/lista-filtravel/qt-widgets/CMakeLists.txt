# A tela numa biblioteca, que o aplicativo e a rotina ligam.
qt_add_library(${CASO}-qt-widgets-tela STATIC Janela.h Janela.cpp Janela.ui ItemProduto.ui)
# O ui_Janela.h e o ui_ItemProduto.h que o uic gera ficam na pasta do autogen da biblioteca.
target_include_directories(${CASO}-qt-widgets-tela PUBLIC .
  "${CMAKE_CURRENT_BINARY_DIR}/${CASO}-qt-widgets-tela_autogen/include")
target_link_libraries(${CASO}-qt-widgets-tela PUBLIC ${CASO}-dominio-cpp Qt6::Widgets)
qt_add_resources(${CASO}-qt-widgets-tela estilo PREFIX / FILES estilo.qss)

qt_add_executable(${CASO}-qt-widgets main.cpp)
target_link_libraries(${CASO}-qt-widgets PRIVATE ${CASO}-qt-widgets-tela)

qt_add_executable(${CASO}-qt-widgets-test test/RoteiroTest.cpp test/Tela.h)
target_link_libraries(${CASO}-qt-widgets-test PRIVATE ${CASO}-qt-widgets-tela Qt6::Test)
add_test(NAME ${CASO}-qt-widgets COMMAND ${CASO}-qt-widgets-test)
set_tests_properties(${CASO}-qt-widgets PROPERTIES ENVIRONMENT QT_QPA_PLATFORM=offscreen)
