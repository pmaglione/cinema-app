import { Component, OnInit } from '@angular/core';
import {ProjectionService} from "../projections.service";
import {AuthenticationService} from "../auth/authentication.service";
import {AppComponent} from "../app.component";

@Component({
  selector: 'app-projection-list',
  templateUrl: './projection-list.component.html',
  styleUrls: ['./projection-list.component.css']
})
export class ProjectionListComponent implements OnInit {
  projections  = [];

  movieText: string;
  cinemaText: string;
  roomText: string;
  dateText: string;
  startTimeText: string;

  constructor(private projectionService: ProjectionService,
              private authenticationService: AuthenticationService,
              public appComponent: AppComponent)
  {
  }

  ngOnInit() {
    this.projectionService.getAllProjections().subscribe(projs => this.projections = projs)
  }

}
