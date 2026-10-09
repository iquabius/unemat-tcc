# O domínio do caso, numa biblioteca que o qt-widgets e a qml ligam.
qt_add_library(${CASO}-dominio-cpp STATIC Dominio.h Dominio.cpp)
target_include_directories(${CASO}-dominio-cpp PUBLIC .)
target_link_libraries(${CASO}-dominio-cpp PUBLIC Qt6::Core)

qt_add_executable(${CASO}-dominio-cpp-test test/DominioTest.cpp test/DataFixa.h)
target_link_libraries(${CASO}-dominio-cpp-test PRIVATE ${CASO}-dominio-cpp Qt6::Test)
add_test(NAME ${CASO}-dominio-cpp COMMAND ${CASO}-dominio-cpp-test)
