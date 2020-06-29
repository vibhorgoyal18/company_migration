import {Component, OnInit} from '@angular/core';
import {MigrationService} from '../../services/migration.service';
import {ServerLoginService} from '../../services/server-login.service';
import {ServerInfoModel} from '../../models/serverInfo.model';
import {MigrationOptionsModel} from '../../models/migrationOptions.model';
import {Router} from '@angular/router';

@Component({
  selector: 'app-verify-details',
  templateUrl: './verify-details.component.html',
  styleUrls: ['./verify-details.component.css']
})
export class VerifyDetailsComponent implements OnInit {

  serverInfo: ServerInfoModel;
  migrationOptions: MigrationOptionsModel;
  migrationOptionsWithLabel = [];

  constructor(
    private serverLoginService: ServerLoginService,
    private router: Router,
    private migrationService: MigrationService
    ) {
  }

  async ngOnInit(): Promise<void> {
    this.serverInfo = {
      source: {
        user: '',
        server: ''
      },
      target: {
        server: '',
        user: '',
      }
    };

    this.serverInfo = await this.serverLoginService.getServerInfo();
    this.migrationOptions = MigrationService.migrationOptions;
    this.migrationOptionsWithLabel = this.migrationService.getMigrationOptionsWithLabel();
  }

  async reset() {
    await this.router.navigate(['server-auth']);
  }

  async migrate() {
    await this.router.navigate(['migrate']);
  }
}
