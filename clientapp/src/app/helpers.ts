export class Helpers {
  static serialize(arr){
      return arr.join(',');
  }

  static unserialize(str){
      return str.split(',');
  }
}
