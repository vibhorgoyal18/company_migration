import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {ServerLoginRequestModel, ServerType} from '../../models/serverLogin.model';
import {ServerLoginService} from '../../services/server-login.service';
import {MatSnackBar} from '@angular/material/snack-bar';

@Component({
  selector: 'app-server-login',
  templateUrl: './server-login.component.html',
  styleUrls: ['./server-login.component.css']
})
export class ServerLoginComponent implements OnInit {
  serverData: ServerLoginRequestModel;
  isSigningIn = false;
  type: ServerType;

  constructor(
    private route: ActivatedRoute,
    private serverLoginSvc: ServerLoginService,
    private snackBar: MatSnackBar,
    private router: Router,
  ) {
  }

  ngOnInit() {
    this.serverData = {
      username: '',
      password: '',
      base_url: '',
      type: this.route.snapshot.queryParamMap.get('type') === '1' ? ServerType.target : ServerType.source
    };

    this.type = this.serverData.type;
  }

  async authenticateServer() {
    try {

      this.isSigningIn = true;
      const loginResponse = await this.serverLoginSvc.login(this.serverData);
      const data = JSON.stringify(loginResponse);
      this.snackBar.open('Login Successful', 'Close', {
        duration: 10000,
        horizontalPosition: 'end',
        verticalPosition: 'top',
      });
      if (this.type === ServerType.source) {
        await this.router.navigate(['create-company']);
      } else {
        await this.router.navigate(['check-options']);
      }
    } catch (error) {
      this.snackBar.open('Login failed', 'Close', {
        duration: 10000,
        horizontalPosition: 'end',
        verticalPosition: 'top',
      });
      this.isSigningIn = false;
    } finally {
      this.isSigningIn = false;
    }
  }
}
