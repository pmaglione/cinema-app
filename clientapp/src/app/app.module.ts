import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
  import { FormsModule, ReactiveFormsModule }   from '@angular/forms';
import { ProjectionFilterPipe } from './projection_filter.pipe';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ProjectionDetailComponent } from './projection-detail/projection-detail.component';
import { ProjectionListComponent } from './projection-list/projection-list.component';
import { HomeComponent } from './home/home.component';
import { WebsocketService } from "./websocket.service";
import { ProjectionService } from "./projections.service";
import { LoginComponent } from "./auth/login.component";
import { RegisterComponent } from "./auth/register.component";
import { JwtInterceptor } from "./auth/jwt.interceptor";
import { ErrorInterceptor } from "./auth/error.interceptor";
import { AlertComponent } from "./alert/alert.component";
import { CheckoutComponent } from './checkout/checkout.component';
import { AuthGuard } from "./auth/auth.guard";

@NgModule({
  declarations: [
    AppComponent,
    ProjectionFilterPipe,
    ProjectionDetailComponent,
    ProjectionListComponent,
    HomeComponent,
    LoginComponent,
    RegisterComponent,
    AlertComponent,
    CheckoutComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    AppRoutingModule,
    ReactiveFormsModule
  ],
  providers: [
    WebsocketService,
    ProjectionService,
    AuthGuard,
    { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
