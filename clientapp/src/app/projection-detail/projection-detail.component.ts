import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import { ProjectionService } from '../projections.service';
import { Projection } from "../models";
import { AppComponent } from "../app.component";
import { Helpers } from "../helpers";
import {AlertService} from "../alert/alert.service";

@Component({
  selector: 'app-projection-detail',
  templateUrl: './projection-detail.component.html',
  styleUrls: ['./projection-detail.component.css']
})
export class ProjectionDetailComponent implements OnInit {

  STATE_FREE = 'FREE';
  STATE_SELECTED = 'SELECTED';
  STATE_OCUPIED = 'OCUPIED';

  projection: Projection;
  rows: number[];
  columns: number[];
  reserved_seats: string[];
  selected_seats: number[];
  toggle_color: boolean[];
  seats_prices: number[];
  total_price: number;
  seat_color: string[];
  seats_availability: boolean[];

  constructor(private projectionService: ProjectionService,
              private route: ActivatedRoute,
              public appComponent: AppComponent,
              private router: Router,
              private alertService: AlertService) {
    this.reserved_seats = [];
    this.selected_seats = [];
    this.toggle_color = [];
    this.seats_prices = [];
    this.total_price = 0;
    this.seat_color = [];
    this.seats_availability = [];
  }

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
     this.projectionService.getProjection(params.get('id')).subscribe(p =>{
        this.rows = [];
        this.columns = [];
        this.reserved_seats = p.reserved_seats.split(',');
        this.seats_prices = p.room.prices.split(',').map(Number);
        this.pushIntArray(this.rows, p.room.num_rows);
        this.pushIntArray(this.columns, p.room.num_columns);
        this.pushArrayVal(this.toggle_color, p.room.num_rows * p.room.num_columns,true);
        this.projection = p;
        this.projectionService.syncProjection(this.projection.id);// WS SUBSCRIPTION
        this.projectionService.projection.subscribe(proj => {
          this.manageUpdate(proj.id, proj.username, proj.reserved_seats);
         });
        this.colorSeats();
      });
    });
  }

  manageUpdate(id, user, seats){
    if (id == this.projection.id && user != this.appComponent.currentUser.username){
      let new_seats_arr = Helpers.unserialize(seats);
      let cancelled = [];
      for (let seat_id of new_seats_arr) {
          this.reserved_seats.push(seat_id);
          this.setSeatOcupied(seat_id);
          if (this.selected_seats.includes(+seat_id)) {
            cancelled.push(seat_id);
            let index: number = this.selected_seats.indexOf(seat_id);
            this.selected_seats.splice(index, 1);
          }
      }
      let seats_cancelled_str = Helpers.serialize(cancelled);
      let alert_msg = "Alert! Some seats were selected by another user";
      this.alertService.error(alert_msg);
      alert(alert_msg);
    }
  }

  setSeatOcupied(seat_id){
    this.setColor(seat_id, this.STATE_OCUPIED);
    this.seats_availability[seat_id] = false;
  }

  book(){
    this.projectionService.projection.next({
      id:this.projection.id,
      username:this.appComponent.currentUser.username,
      seats:Helpers.serialize(this.selected_seats),
      action:'book'
    });
    this.router.navigate(['/checkout']);
  }

  pushIntArray = function(attr, num) {
    for (let i = 0; i < num; i++) {
      attr.push(i);
    }
  };

  pushArrayVal = function(attr, num, val) {
    for (let i = 0; i < num; i++) {
      attr.push(val);
    }
  };

  manageSeat(seat_id) {
    if (this.selected_seats.includes(seat_id)){
      const index: number = this.selected_seats.indexOf(seat_id);
      if (index !== -1) {
          this.selected_seats.splice(index, 1);
          this.total_price -= +this.seats_prices[seat_id];
          this.setColor(seat_id, this.STATE_FREE);
      }
    } else {
      this.selected_seats.push(seat_id);
      this.toggle_color[seat_id] = !this.toggle_color[seat_id];
      this.total_price += +this.seats_prices[seat_id];
      this.setColor(seat_id, this.STATE_SELECTED);
    }
  }

  colorSeats() {
    let amount_seats = this.projection.room.num_rows * this.projection.room.num_columns;
    for (let _id = 0; _id < amount_seats; _id++) {
      let seat_id = _id.toString();
      if (!this.reserved_seats.includes(seat_id) && !this.selected_seats.includes(_id)) {
        this.setColor(seat_id, this.STATE_FREE);
        this.seats_availability[_id] = true;
      } else if (!this.reserved_seats.includes(seat_id) && this.selected_seats.includes(_id)) {
        this.setColor(seat_id, this.STATE_SELECTED);
        this.seats_availability[_id] = true;
      } else if (this.reserved_seats.includes(seat_id)) {
        this.setColor(seat_id, this.STATE_OCUPIED);
        this.seats_availability[_id] = false;
      }
    }
  }

  setColor(i, state){
    switch(state) {
       case this.STATE_FREE: {
          this.seat_color[i] = '#36c45a';
          break;
       }
       case this.STATE_SELECTED: {
          this.seat_color[i] = '#ffc107';
          break;
       }
       case this.STATE_OCUPIED: {
          this.seat_color[i] = '#ea1932';
          break;
       }
    }
  }
}
