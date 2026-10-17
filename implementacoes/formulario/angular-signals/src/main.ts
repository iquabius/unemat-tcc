import { provideBrowserGlobalErrorListeners } from "@angular/core";
import { bootstrapApplication } from "@angular/platform-browser";
import { FormularioDeCompra } from "./app/formulario";

bootstrapApplication(FormularioDeCompra, {
  providers: [provideBrowserGlobalErrorListeners()],
}).catch((err) => console.error(err));
