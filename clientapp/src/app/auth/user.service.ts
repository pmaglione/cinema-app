import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { User } from '../models';
import { environment } from "../../environments/environment";

@Injectable({ providedIn: 'root' })
export class UserService {
    constructor(private http: HttpClient) { }

    getById(id: number) {
        return this.http.get(`${environment.BASE_URL}/users/${id}`);
    }

    register(user: User) {
        return this.http.post(`${environment.BASE_URL}/rest-auth/registration/`, user);
    }
}
