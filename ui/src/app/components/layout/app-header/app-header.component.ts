import { Component, OnInit } from '@angular/core';
import { MenuItem, PrimeIcons } from 'primeng/api';
import { UserService } from 'src/app/services/users.service';
import { ConfirmationService } from 'primeng/api';

@Component({
    selector: 'app-header',
    templateUrl: './app-header.component.html',
    styleUrls: ['./app-header.component.css'],
    providers: [ConfirmationService]
})
export class AppHeaderComponent implements OnInit {

    items: MenuItem[];
    buttonText: String = "Log In";
    loginVisible: boolean = false;

    constructor(private userService: UserService, private confirmationService: ConfirmationService) { }

    ngOnInit(): void {
        this.items = [
            {
                label: 'Authors', icon: PrimeIcons.USER,
                items: [
                    {
                        label: 'Popular',
                        routerLink: ['/authors/popular']
                    }
                ]
            },
            {
                label: 'Blogs', icon: PrimeIcons.BOOK,
                items: [
                    {
                        label: 'Popular',
                        routerLink: ['/blogs/popular']
                    }
                ]
            }
        ]
    }

    confirm(header: string, message: string, icon: string) {
        this.confirmationService.confirm({
            header: header,
            message: message,
            icon: icon,
            acceptLabel: 'OK',
            rejectVisible: false,
        });
    }

    signinResult(value: string) {
        this.loginVisible = false;
        switch (value) {
            case "Log In Success":
                this.buttonText = "Log Out"
                break;
            case "Log In Failure":
                this.confirm("Error", "Log In Failed!",'pi pi-exclamation-triangle');
                break;
            case "Register Success":
                this.confirm("Registered", "Registration was successful.  You may now log in.", 'pi pi-info')
                break;
            case "Register Failure":
                this.confirm("Error", "Registration Failed!",'pi pi-exclamation-triangle');
                break;
            case "Register Username":
                this.confirm("Error", "Registration Failed!  Username is already used.",'pi pi-exclamation-triangle');
                break;
            case "Register Email":
                this.confirm("Error", "Registration Failed!  Email is already used.",'pi pi-exclamation-triangle');
                break;
            case "Cancelled":
                break;
            default:
                break;
        }
    }

    handleLogOnOff(e: Event) {
        if (this.buttonText == "Log In") {
            this.loginVisible = true;
            // Signin/Register is modal, so result will come from signinResult()
        } else {
            this.userService.logout().subscribe();
            this.buttonText = "Log In";
        }
    }

}
