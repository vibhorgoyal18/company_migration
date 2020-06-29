import {Component, OnInit} from '@angular/core';
import {MigrationOptionsModel} from '../../models/migrationOptions.model';
import {MigrationService} from '../../services/migration.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-check-options',
  templateUrl: './check-options.component.html',
  styleUrls: ['./check-options.component.css']
})
export class CheckOptionsComponent implements OnInit {
  migrationOptions: MigrationOptionsModel;


  constructor(private router: Router) {
  }

  ngOnInit(): void {
    this.migrationOptions = {
      isCheckedEnvironmentVariables: true,
      isCheckedPublishProcessBeforeMigration: true,
      isCheckedCompanySettings: true,
      isCheckedPublishProcessPostMigration: true,
      isCheckedAddAndAssignDummyHubToAdmin: true,
      isCheckedMigrateDataStore: true,
      isCheckedUpdatePostHookUrl: false,
      isCheckedCitiesBranches: false,
      isCheckedGeoLocation: false,
      isCheckedVehicleConfiguration: false,
      isCheckedUsers: false,
    };
  }

  async setMigrationOptions()  {
    MigrationService.migrationOptions = this.migrationOptions;
    await this.router.navigate(['verify-details']);

  }
}
