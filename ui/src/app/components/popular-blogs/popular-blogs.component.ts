import { Component, OnInit } from '@angular/core';
import { Blog } from 'src/app/interfaces/blog';
import { BlogService } from 'src/app/services/blogs.service';

@Component({
    selector: 'app-popular-blogs',
    templateUrl: './popular-blogs.component.html',
    styleUrls: ['./popular-blogs.component.css']
})
export class PopularBlogsComponent implements OnInit {

    popularBlogs: [Blog];

    constructor(private blogService: BlogService) { }

    ngOnInit(): void {
        this.blogService.popular()
            .subscribe(
                result => {
                    this.popularBlogs = result;
                }
            );
    }

}
