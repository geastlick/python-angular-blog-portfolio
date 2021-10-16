import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { HttpClientModule } from '@angular/common/http'

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import {PanelModule} from 'primeng/panel';
import {ScrollPanelModule} from 'primeng/scrollpanel';
import {SplitterModule} from 'primeng/splitter';
import {ReactiveFormsModule } from '@angular/forms';
import {AccordionModule} from 'primeng/accordion';
import {MenubarModule} from 'primeng/menubar';
import {ButtonModule} from 'primeng/button';
import {DialogModule} from 'primeng/dialog';
import {TabViewModule} from 'primeng/tabview';
import {InputTextModule} from 'primeng/inputtext';
import {InputTextareaModule} from 'primeng/inputtextarea';
import {ConfirmPopupModule} from 'primeng/confirmpopup';
import {ConfirmDialogModule} from 'primeng/confirmdialog';

import { AppHeaderComponent } from './layout/app-header/app-header.component';
import { AppFooterComponent } from './layout/app-footer/app-footer.component';
import { AppLeftNavComponent } from './layout/app-left-nav/app-left-nav.component';
import { UserService } from './services/users.service';
import { HttpErrorHandler } from './http-error-handler.service';
import { ErrorMessageService } from './error-message.service';
import { SigninComponent } from './signin/signin.component';
import { RegisterComponent } from './register/register.component';
import { SigninRegisterComponent } from './signin-register/signin-register.component';
import { PopularBlogsComponent } from './popular-blogs/popular-blogs.component';
import { BlogCardComponent } from './blog-card/blog-card.component'

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
    BlogCardComponent
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
    AccordionModule,
    MenubarModule,
    ButtonModule,
    DialogModule,
    TabViewModule,
    InputTextModule,
    InputTextareaModule,
    ConfirmPopupModule,
    ConfirmDialogModule,
  ],
  providers: [UserService, HttpErrorHandler, ErrorMessageService],
  bootstrap: [AppComponent]
})
export class AppModule { }
