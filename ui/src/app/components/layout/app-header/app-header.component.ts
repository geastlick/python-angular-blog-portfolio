import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { MenuItem, PrimeIcons } from 'primeng/api';
import { UserService } from 'src/app/services/users.service';
import { ConfirmationService } from 'primeng/api';
import { NavigationEnd, Router } from '@angular/router';

@Component({
    selector: 'app-header',
    templateUrl: './app-header.component.html',
    styleUrls: ['./app-header.component.css'],
    providers: [ConfirmationService]
})
export class AppHeaderComponent implements OnInit {

    items: MenuItem[];

    crumbs: MenuItem[] = [];
    home: MenuItem;

    buttonText: String = "Log In";
    loginVisible: boolean = false;

    constructor(private userService: UserService,
        private confirmationService: ConfirmationService,
        private router: Router,
        private ref: ChangeDetectorRef) { }

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
        ];

        this.home = { icon: 'pi pi-home', routerLink: '/' }

        this.router.events.subscribe(event => {
            if (event instanceof NavigationEnd) { this.breadcrumb(event) }
        });
    }

    breadcrumb(event: NavigationEnd) {
        let url = event.urlAfterRedirects;
        let reurl = url.replace(/\/[0-9]+\//g, "/id/");
        reurl = url.replace(/\/[0-9]+$/, "/id");
        switch (reurl) {
            case "/authors/popular": this.crumbs = []; this.crumbs.push({ label: "PopularAuthors", routerLink: "authors/popular" }); break;
            case "/": this.crumbs = []; break;
            case "/blogs/popular": this.crumbs = []; this.crumbs.push({ label: "PopularBlogs", routerLink: "/blogs/popular" }); break;
            case "/blogs/id": this.crumbs.push({ label: "Blog", routerLink: url }); break;
        }
        this.crumbs = this.crumbs.slice(0);
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
                this.confirm("Error", "Log In Failed!", 'pi pi-exclamation-triangle');
                break;
            case "Register Success":
                this.confirm("Registered", "Registration was successful.  You may now log in.", 'pi pi-info')
                break;
            case "Register Failure":
                this.confirm("Error", "Registration Failed!", 'pi pi-exclamation-triangle');
                break;
            case "Register Username":
                this.confirm("Error", "Registration Failed!  Username is already used.", 'pi pi-exclamation-triangle');
                break;
            case "Register Email":
                this.confirm("Error", "Registration Failed!  Email is already used.", 'pi pi-exclamation-triangle');
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
