import { provideBrowserGlobalErrorListeners } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { FormularioDeReserva } from './app/formulario';

bootstrapApplication(FormularioDeReserva, {
  providers: [provideBrowserGlobalErrorListeners()],
}).catch((err) => console.error(err));
