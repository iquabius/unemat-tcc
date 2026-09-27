import { provideBrowserGlobalErrorListeners } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { CatalogoDeProdutos } from './app/catalogo';

bootstrapApplication(CatalogoDeProdutos, {
  providers: [provideBrowserGlobalErrorListeners()],
}).catch((err) => console.error(err));
