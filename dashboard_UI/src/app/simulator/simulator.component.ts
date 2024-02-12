import { Component, OnInit, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormGroup , FormControl } from '@angular/forms';
import { NgxChartsModule } from '@swimlane/ngx-charts';

import { GeneratorService } from '../services/generator.service';


// type MyArrayType = Array<{id: string, displayName: string}>;
// type myDictType = {id: string, displayName: string}

@Component({
  selector: 'app-simulator',
  templateUrl: './simulator.component.html',
  styleUrls: ['./simulator.component.css']
})
export class SimulatorComponent implements OnInit {


  selectedScenario: string = "Casual Interactions";
  scenarios: string[] = ['Casual Interactions', 'Total lockdown',
  // 'Friends Interaction', 'Birthday Celebrations', 'Vaccination', 'Mutations'
];

  // addOns: string[] = [];

  population: number = 1000;
  is_population_generated: boolean = false;
  is_population_generating: boolean = false;
  is_simulation_done: boolean = false;
  is_running_simulation: boolean = false;

  disabled: boolean = false;
  checked_friends_interation: boolean = false;
  checked_birthday: boolean = false;
  checked_vaccination: boolean = false;
  checked_mutations: boolean = false;



  // multi: any[];
  view: number[] = [700, 300];

  // options
  legend: boolean = true;
  showLabels: boolean = true;
  animations: boolean = true;
  xAxis: boolean = true;
  yAxis: boolean = true;
  showYAxisLabel: boolean = true;
  showXAxisLabel: boolean = true;
  xAxisLabel: string = 'Days';
  yAxisLabel: string = 'Number of People';
  timeline: boolean = true;

  graph_data: any = []

  colorScheme = {
    domain: ['#5AA454', '#E44D25', '#CFC0BB', '#7aa3e5', '#a8385d', '#aae3f5']
  };


  probabilities = [
    {"name": "School Going Probability", "display": "Probability of Going to School", 'displayNone':"Total lockdown", "value": 0.4},
    {"name": "Work Going Probability", "display": "Probability of Going to Work", 'displayNone':"Total lockdown", "value": 0.4},
    {"name": "Dog Walking Probability", "display": "Probability of Walking a Dog", 'displayNone':"", "value": 0.6},
    {"name": "Prayer Group Probability", "display": "Probability of religious activities(Church, temple, mosque etc)", 'displayNone':"Total lockdown", "value": 0.5},
    {"name": "Volunteer Group Probability", "display": "Probability of Working in a Volunteer Group", 'displayNone':"", "value": 0.6},
    {"name": "Play Sports Probability",  "display": "Probability of playing sports", 'displayNone':"Total lockdown", "value": 0.6},
    {"name": "Grocery Probability", "display": "Probability of Buying Groceries", 'displayNone':"", "value": 0.4},
    {"name": "Gas Probability", "display": "Probability of Filling up gas", 'displayNone':"", "value": 0.4},
    {"name": "Mall Probability", "display": "Probability of visiting a Mall", 'displayNone':"Total lockdown", "value": 0.4},
  ]

  school_prob = 0.4
  work_prob = 0.4
  dog_walk_prob = 0.6



  constructor(
    private generatorService: GeneratorService
  ) {
    // Object.assign(this, { multi });
  }

  ngOnInit(): void {
  }



  formatLabel(value: number) {
    if (value >= 1000) {
      return Math.round(value / 100) / 10 + 'k';
    }
    this.is_population_generated = false;
    return value;

  }

  formatLabelprobability(value: number){
    return value;
  }

  simulateVirus() {
    this.is_simulation_done = false;
    this.is_running_simulation = true;
    let probability_dict: {[key:string]: any} = {}
    this.probabilities.forEach(probability => {
      probability_dict[probability["name"]] = probability["value"];
    });
    probability_dict["population"] = this.population;
    probability_dict["scenario"] = this.selectedScenario;
    this.generatorService.simulateVirus(probability_dict).subscribe((data) => {
      this.is_simulation_done = true;
      this.is_running_simulation = false;
      console.log(data);
      this.graph_data = data;
      console.log(this.graph_data['Data']);
    });
  }

  createPopulation() {
    this.is_population_generating = true;
    this.generatorService.generatePopulation(this.population).subscribe((data) => {
      this.is_population_generated = true;
      this.is_population_generating = false;

    });
  }


  // onSelect(data): void {
  //   console.log('Item clicked', JSON.parse(JSON.stringify(data)));
  // }
  //
  // onActivate(data): void {
  //   console.log('Activate', JSON.parse(JSON.stringify(data)));
  // }
  //
  // onDeactivate(data): void {
  //   console.log('Deactivate', JSON.parse(JSON.stringify(data)));
  // }

}
