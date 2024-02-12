import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpParams  } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class GeneratorService {

  private REST_API_SERVER = "http://127.0.0.1:8000";

  constructor(private httpClient: HttpClient) { }

  public generatePopulation(population: number){
    return this.httpClient.post(this.REST_API_SERVER + "/generate", {"population": population});
  }

  public simulateVirus(data: any){
    return this.httpClient.post(this.REST_API_SERVER + "/simulate", data);
  }


}
