# Projeto CMake único dos casos no Qt, como o projeto Gradle de casos/android/.
# Cada caso pode ter três pastas, ao lado das implementações web:
#   dominio-cpp/  o porte do dominio.ts, compartilhado pelas duas tecnologias;
#   qt-widgets/   Qt Widgets: tela em .ui, signals e slots em C++;
#   qml/          QML: tela e property bindings em QML.
# O projeto inclui sozinho toda pasta dessas que tenha CMakeLists.txt, e os
# alvos se chamam <caso>-<pasta> (por exemplo, formulario-qt-widgets).
#
# Uso, de casos/qt/:
#   cmake -S . -B build -G Ninja && cmake --build build
#   QT_QPA_PLATFORM=offscreen ctest --test-dir build --output-on-failure
cmake_minimum_required(VERSION 3.21)
project(casos-qt LANGUAGES CXX)

find_package(Qt6 6.5 REQUIRED COMPONENTS Core Gui Widgets Qml Quick QuickControls2 Test)
qt_standard_project_setup(REQUIRES 6.5)
# Os componentes de estilo de cada tela QML ficam numa subpasta do módulo.
qt_policy(SET QTP0004 NEW)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
enable_testing()

file(GLOB casos LIST_DIRECTORIES true "${CMAKE_CURRENT_SOURCE_DIR}/../*")
list(SORT casos)
foreach(pasta_do_caso IN LISTS casos)
  get_filename_component(caso "${pasta_do_caso}" NAME)
  # O domínio primeiro: as duas tecnologias ligam com ele.
  foreach(tecnologia IN ITEMS dominio-cpp qt-widgets qml)
    if(EXISTS "${pasta_do_caso}/${tecnologia}/CMakeLists.txt")
      set(CASO "${caso}")
      add_subdirectory("${pasta_do_caso}/${tecnologia}" "${caso}-${tecnologia}")
    endif()
  endforeach()
endforeach()
