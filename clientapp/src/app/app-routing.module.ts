import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { ProjectionDetailComponent } from './projection-detail/projection-detail.component';
import { ProjectionListComponent } from "./projection-list/projection-list.component";
import { HomeComponent } from "./home/home.component";
import { LoginComponent } from "./auth/login.component";
import { RegisterComponent } from "./auth/register.component";
import { CheckoutComponent } from "./checkout/checkout.component";
import { AuthGuard } from "./auth/auth.guard";

const routes: Routes = [
    {path: 'login', component: LoginComponent },
    {path: 'register', component: RegisterComponent },
    {path: 'projections' , component: ProjectionListComponent},
    {path: 'projection/:id' , component: ProjectionDetailComponent, pathMatch: 'full', canActivate: [AuthGuard]},
    {path: 'checkout' , component: CheckoutComponent, canActivate: [AuthGuard]},

    // always last directive!
    {path: '**' , component: HomeComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
