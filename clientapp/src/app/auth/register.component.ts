import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';
import { HttpResponse } from "@angular/common/http";
import { AlertService } from "../alert/alert.service";
import { UserService } from "./user.service";
import { AuthenticationService } from "./authentication.service";
import { User } from "../models";


@Component({ templateUrl: 'register.component.html' })
export class RegisterComponent implements OnInit {
    registerForm: FormGroup;
    loading = false;
    submitted = false;

    constructor(
        private formBuilder: FormBuilder,
        private router: Router,
        private authenticationService: AuthenticationService,
        private userService: UserService,
        private alertService: AlertService
    ) {
        // redirect to home if already logged in
        if (this.authenticationService.currentUserValue) {
            this.router.navigate(['/']);
        }
    }

    ngOnInit() {
        this.registerForm = this.formBuilder.group({
            username: ['', Validators.required],
            email: ['', [Validators.required, Validators.email]],
            password1: ['', [Validators.required, Validators.minLength(6)]]
        });
    }

    // convenience getter for easy access to form fields
    get f() { return this.registerForm.controls; }

    onSubmit() {
        this.submitted = true;

        // reset alerts on submit
        this.alertService.clear();

        // stop here if form is invalid
        if (this.registerForm.invalid) {
            return;
        }

        this.loading = true;

        let user = new User();
        let form = this.registerForm.value;
        user.username = form.username;
        user.email = form.email;
        user.password1 = form.password1;
        user.password2 = form.password1;

        this.userService.register(user)
            .pipe(first())
            .subscribe(
                data => {
                  this.navSucess();
                },
                error => {
                    if (error.status === 500) {
                      this.navSucess();

                    } else {
                      this.alertService.error(this.getUserErrors(error));
                      this.loading = false;
                    }
                });
    }

    navSucess(){
      this.alertService.success('Registration successful', true);
      this.router.navigate(['/login']);
    }

    getUserErrors(response){
      let errors = "";
      if (response.username != undefined){
        errors += response.username +"\n";
      }
      if (response.email != undefined){
        errors += response.email +"\n";
      }
      if (response.password != undefined){
        errors += response.password +"\n";
      }

      return errors
    }
}
