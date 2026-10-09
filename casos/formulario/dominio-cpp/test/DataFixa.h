#pragma once

#include "Dominio.h"

// Fixa "hoje" em 26/09/2026 enquanto existir, a mesma data que o script de
// capturas fixa na web; como a regra DataFixa do Kotlin.
struct DataFixa {
    DataFixa() { formulario::relogio = [] { return QDate(2026, 9, 26); }; }
    ~DataFixa() { formulario::relogio = [] { return QDate::currentDate(); }; }
};
