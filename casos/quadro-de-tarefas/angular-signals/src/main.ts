import { provideBrowserGlobalErrorListeners } from "@angular/core";
import { bootstrapApplication } from "@angular/platform-browser";
import { QuadroDeTarefas } from "./app/quadro";

bootstrapApplication(QuadroDeTarefas, {
  providers: [provideBrowserGlobalErrorListeners()],
}).catch((err) => console.error(err));
