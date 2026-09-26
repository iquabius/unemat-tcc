import { provideBrowserGlobalErrorListeners } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { BuscaDeDestino } from './app/busca';

bootstrapApplication(BuscaDeDestino, {
  providers: [provideBrowserGlobalErrorListeners()],
}).catch((err) => console.error(err));
