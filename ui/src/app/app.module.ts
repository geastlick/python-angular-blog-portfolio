import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { HttpClientModule } from '@angular/common/http'

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { PanelModule } from 'primeng/panel';
import { ScrollPanelModule } from 'primeng/scrollpanel';
import { SplitterModule } from 'primeng/splitter';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { AccordionModule } from 'primeng/accordion';
import { MenubarModule } from 'primeng/menubar';
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { TabViewModule } from 'primeng/tabview';
import { InputTextModule } from 'primeng/inputtext';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { ConfirmPopupModule } from 'primeng/confirmpopup';
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { TableModule } from 'primeng/table';
import { CardModule } from 'primeng/card';
import { AvatarModule } from 'primeng/avatar';
import { RatingModule } from 'primeng/rating';
import {ProgressSpinnerModule} from 'primeng/progressspinner';


import { AppHeaderComponent } from './components/layout/app-header/app-header.component';
import { AppFooterComponent } from './components/layout/app-footer/app-footer.component';
import { AppLeftNavComponent } from './components/layout/app-left-nav/app-left-nav.component';
import { UserService } from './services/users.service';
import { HttpErrorHandler } from './services/http-error-handler.service';
import { ErrorMessageService } from './services/error-message.service';
import { SigninComponent } from './components/security/signin/signin.component';
import { RegisterComponent } from './components/security/register/register.component';
import { SigninRegisterComponent } from './components/security/signin-register/signin-register.component';
import { PopularBlogsComponent } from './components/popular-blogs/popular-blogs.component';
import { BlogCardComponent } from './components/blog-card/blog-card.component'
import { BlogService } from './services/blogs.service';
import { BlogComponent } from './components/blog/blog.component';
import { BlogEntryService } from './services/blog-entries.service';
import { EntryCardComponent } from './components/entry-card/entry-card.component';
import { PopularAuthorsComponent } from './components/popular-authors/popular-authors.component';

@NgModule({
    declarations: [
        AppComponent,
        AppHeaderComponent,
        AppFooterComponent,
        AppLeftNavComponent,
        SigninComponent,
        RegisterComponent,
        SigninRegisterComponent,
        PopularBlogsComponent,
        BlogCardComponent,
        BlogComponent,
        EntryCardComponent,
        PopularAuthorsComponent
    ],
    imports: [
        BrowserModule,
        HttpClientModule,
        BrowserAnimationsModule,
        AppRoutingModule,
        PanelModule,
        ScrollPanelModule,
        SplitterModule,
        ReactiveFormsModule,
        FormsModule,
        AccordionModule,
        MenubarModule,
        ButtonModule,
        DialogModule,
        TabViewModule,
        InputTextModule,
        InputTextareaModule,
        ConfirmPopupModule,
        ConfirmDialogModule,
        TableModule,
        CardModule,
        AvatarModule,
        RatingModule,
        ProgressSpinnerModule,
    ],
    providers: [
        UserService,
        BlogService,
        BlogEntryService,
        HttpErrorHandler,
        ErrorMessageService
    ],
    bootstrap: [AppComponent]
})
export class AppModule { }
