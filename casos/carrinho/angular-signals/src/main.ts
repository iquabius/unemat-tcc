import { provideBrowserGlobalErrorListeners } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { Loja } from './app/loja';

bootstrapApplication(Loja, {
  providers: [provideBrowserGlobalErrorListeners()],
}).catch((err) => console.error(err));
