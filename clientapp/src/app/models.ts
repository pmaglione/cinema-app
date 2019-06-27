export class Projection{
  id: number;
  movie:string;
  room:Room;
  cinema:Cinema;
  date:string;
  start_time:string;
  end_time:string;
  reserved_seats:string;

  public constructor(init?:Partial<Projection>) {
        Object.assign(this, init);
  }
}

export class Room {
  id:number;
  number:number;
  cinema:Cinema;
  num_rows:number;
  num_columns:number;
  prices:string;
}

export class Cinema {
  id:number;
  name:string;
}

export class Movie {
  id:number;
  name:string;
  year:number;
}

export class Reservation {
  author: User;
  state: ReservationState
  projection: Projection;
  created_date: string;
  seats: string;
}

export class ReservationState{
  id:number;
  name:string;
}

export class ReservationSubject {
  id:number;
  reserved_seats:string;
  username:string;
}

export class RegistrationUser {
  username:string;
  email:string;
  password1:string;
  password2:string;
}

export class User {
  id: number;
  username: string;
  email:string;
  password1: string;
  password2: string;
  token: string;
}


