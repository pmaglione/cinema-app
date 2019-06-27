import { Pipe, PipeTransform } from '@angular/core';
@Pipe({
  name: 'projection_filter'
})

export class ProjectionFilterPipe implements PipeTransform {
    transform(items: any[], movie: string, cinema: string, room: string, date:string, start_time: string){
        if (!items) return [];
          if (movie){
            movie = movie.toLowerCase();
            items = [...items.filter(item => item.movie.name.toLowerCase().indexOf(movie.toLowerCase()) !== -1)];
          }

          if (cinema){
            cinema = cinema.toLowerCase();
            items = [...items.filter(item => item.room.cinema.name.toLowerCase().indexOf(cinema.toLowerCase()) !== -1)];
          }

          if (room){
            room = room.toLowerCase();
            items = [...items.filter(item => item.room.number.toString().toLowerCase().indexOf(room.toLowerCase()) !== -1)];
          }

          if (date){
            date = date.toLowerCase();
            items = [...items.filter(item => item.date.toLowerCase().indexOf(date.toLowerCase()) !== -1)];
          }


          if (start_time){
            start_time = start_time.toLowerCase();
            items = [...items.filter(item => item.start_time.toLowerCase().indexOf(start_time.toLowerCase()) !== -1)];
          }

          return items;
        }
}

