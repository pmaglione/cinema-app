import { Component, OnInit } from '@angular/core';
import { AppComponent } from "../app.component";
import { ProjectionService } from "../projections.service";
import {AuthenticationService} from "../auth/authentication.service";
import { Helpers } from "../helpers";
import {Router} from "@angular/router";
import {first} from "rxjs/operators";
import { AlertService } from "../alert/alert.service";

@Component({
  selector: 'app-checkout',
  templateUrl: './checkout.component.html',
  styleUrls: ['./checkout.component.css']
})
export class CheckoutComponent implements OnInit {

  reservations  = [];

  constructor(private projectionService: ProjectionService,
              private appComponent: AppComponent,
              private router: Router,
              private alertService: AlertService) { }

  ngOnInit() {
    this.loadReservations();
  }

  loadReservations() {
    this.projectionService
      .getUserReservations(this.appComponent.currentUser.username)
      .subscribe(res => this.reservations = res)
  }

  getPrice(seats_str, prices_str) {
    let seats_arr = Helpers.unserialize(seats_str);
    let prices_arr = Helpers.unserialize(prices_str);
    let amt = 0;
    for (let seat_id of seats_arr) {
      amt += +prices_arr[seat_id];
    }

    return +amt;
  }

  checkout(reservation_id) {
    this.projectionService.checkoutReservation(reservation_id)
            .pipe(first())
            .subscribe(
                data => {
                  this.alertService.success('Checkout successful', true);
                  this.loadReservations();
                },
                error => {
                      this.alertService.error(error.error);
                });
  }

  cancel(reservation_id) {
    this.projectionService.cancelReservation(reservation_id)
            .pipe(first())
            .subscribe(
                data => {
                  this.alertService.success('Cancellation successful', true);
                  this.loadReservations();
                },
                error => {
                      this.alertService.error(error.error);
                });
  }

  showByState(state) {
    if (state == 'selected') {
      return true;
    } else {
      return false;
    }
  }
}
