import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {ServerLoginRequestModel, ServerType} from '../../models/serverLogin.model';
import {CreateCompanyModel} from '../../models/createCompany.model';

@Component({
  selector: 'app-create-company',
  templateUrl: './create-company.component.html',
  styleUrls: ['./create-company.component.css']
})
export class CreateCompanyComponent implements OnInit {

  hasCompany = false;
  userName = '';
  password = '';
  code: '';
  email: string;
  phone: string;

  constructor(
    private router: Router,
    private route: ActivatedRoute
  ) {
  }

  ngOnInit(): void {

  }

  showCreateDialog() {
    this.hasCompany = !this.hasCompany;
  }

  async navigateToServerCredentials() {
    await this.router.navigate(['server-auth'], {queryParams: {type: 1}});
  }
}
