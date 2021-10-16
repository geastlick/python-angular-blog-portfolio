import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PopularBlogsComponent } from './components/popular-blogs/popular-blogs.component';


const routes: Routes = [
    { path: '', pathMatch: 'full', component: PopularBlogsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
