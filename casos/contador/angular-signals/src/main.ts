import { provideBrowserGlobalErrorListeners } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { Contador } from './app/contador';

bootstrapApplication(Contador, {
  providers: [provideBrowserGlobalErrorListeners()],
}).catch((err) => console.error(err));
