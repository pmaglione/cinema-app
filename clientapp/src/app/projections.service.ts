import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import {Projection, ReservationSubject, Reservation, User} from "./models";
import { Observable, Subject } from "rxjs";
import { environment } from "../environments/environment";
import {WebsocketService} from "./websocket.service";
import { map } from 'rxjs/operators'


const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type':  'application/json',
    'Authorization': 'my-auth-token'
  })
};

@Injectable({
  providedIn: 'root'
})
export class ProjectionService {
  private reservationsPath = "/reservations";

  public projection: Subject<any>;

  constructor(private http: HttpClient, private wsService: WebsocketService) {
  }

  syncProjection(id){
    this.projection = <Subject<any>>this.wsService
      .connect(environment.PROJECTION_WS_URL + id + '/')
      .pipe(map((response:MessageEvent): Object => {
        let data = JSON.parse(response.data);
        let res = new ReservationSubject();
        res.id = data.id;
        res.reserved_seats = data.reserved_seats;
        res.username = data.username;
        return res;
      }));
  }

  getAllProjections() {
    return this.http.get<Projection[]>(environment.BASE_URL + this.reservationsPath + "/all");
  }

  getProjection(id) {
    return this.http.get<Projection>(environment.BASE_URL + this.reservationsPath + "/get/" + id + '/');
  }

  getUserReservations (username: string): Observable<Reservation[]> {
    return this.http.get<Reservation[]>(environment.BASE_URL + this.reservationsPath + '/get_by_username/' + username + "/");
  }

  checkoutReservation(reservation_id: number) {
    return this.http.post(environment.BASE_URL + this.reservationsPath + "/checkout/"+reservation_id+"/", {});
  }

  cancelReservation(reservation_id: number) {
    return this.http.post(environment.BASE_URL + this.reservationsPath + "/cancel/"+reservation_id+"/", {});
  }
}
