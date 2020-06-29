import {Component, OnDestroy, OnInit} from '@angular/core';
import {MigrationService} from '../../services/migration.service';
import {faClock, faCheck, faTimes} from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-migrate',
  templateUrl: './migrate.component.html',
  styleUrls: ['./migrate.component.css']
})
export class MigrateComponent implements OnInit, OnDestroy {
  migrationOptions: any;
  pending = faClock;
  completed = faCheck;
  failed = faTimes;


  constructor(private migrationService: MigrationService) {
  }

  async ngOnInit(): Promise<void> {
    this.migrationService.timerOption.next('start')
    const migrationOptions = this.migrationService.getMigrationOptionsWithLabel();

    migrationOptions.forEach(migrationOption => {
      migrationOption.status = Status.pending;
    });
    this.migrationOptions = [...migrationOptions];

    for (const migrationOption of migrationOptions) {
      migrationOption.status = Status.inProgress;
      this.migrationOptions = [...migrationOptions];
      if (migrationOption.isChecked) {
        try {
          switch (migrationOption.migrationOptionKey) {
            case 'UserTypesAndRoles':
              await this.migrationService.migrateUserTypes();
              break;
            case 'EnvironmentVariables':
              await this.migrationService.migrateEnvVariables();
              break;
            case 'CompanySettings':
              await this.migrationService.migrateCompanySettings();
              break;
            case 'PublishProcessBeforeMigration':
              await this.migrationService.publishProcesses();
              break;
            case 'PublishProcessPostMigration':
              await this.migrationService.publishProcesses();
              break;
            case 'UpdatePostHookUrl':
              await this.migrationService.updatePostHookUrl();
              break;
            case 'AddAndAssignDummyHubToAdmin':
              await this.migrationService.addAndAssignBranchToAdmin();
              break;
            case 'MigrateDataStore':
              await this.migrationService.migrateDataStore();
              await this.migrationService.migrateDataStore();
              break;
          }
          migrationOption.status = Status.completed;
          this.migrationOptions = [...migrationOptions];
        } catch (error) {
          migrationOption.status = Status.failed;
          this.migrationOptions = [...migrationOptions];
        }
      }
    }
    this.migrationService.timerOption.next('pause');
  }

  ngOnDestroy(): void {
    this.migrationService.timerOption.next('stop')
  }
}

enum Status {
  pending,
  inProgress,
  completed,
  failed
}
