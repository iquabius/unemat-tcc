import { provideBrowserGlobalErrorListeners } from "@angular/core";
import { bootstrapApplication } from "@angular/platform-browser";
import { LoginComQuarentena } from "./app/login";

bootstrapApplication(LoginComQuarentena, {
  providers: [provideBrowserGlobalErrorListeners()],
}).catch((err) => console.error(err));
