import {Component, OnDestroy, OnInit} from '@angular/core';
import {countUpTimerConfigModel, CountupTimerService, timerTexts} from "ngx-timer";
import {Event, NavigationEnd, NavigationStart, Router} from "@angular/router";
import {MigrationService} from "../../services/migration.service";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit, OnDestroy {

  timerOption = 'stop';
  constructor(
    private countUpTimerService: CountupTimerService,
    private migrationService: MigrationService
  ) {
  }

  ngOnDestroy(): void {
    this.countUpTimerService.stopTimer();
  }

  testConfig: countUpTimerConfigModel;

  ngOnInit(): void {
    this.testConfig = new countUpTimerConfigModel();
    this.testConfig.timerClass = 'test_Timer_class';
    this.testConfig.timerTexts = new timerTexts();
    this.testConfig.timerTexts.hourText = " :";
    this.testConfig.timerTexts.minuteText = " :";
    this.testConfig.timerTexts.secondsText = " ";

    this.migrationService.timerOption.subscribe(timerOption => {
      this.timerOption = timerOption
      timerOption === 'start'
      if(timerOption === 'start')
        this.countUpTimerService.startTimer();
      else if(timerOption === 'pause')
        this.countUpTimerService.pauseTimer();
      else
        this.countUpTimerService.stopTimer();
    })
  }
}
