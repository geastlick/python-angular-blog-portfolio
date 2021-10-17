import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Blog } from 'src/app/interfaces/blog';
import { BlogEntry } from 'src/app/interfaces/blog-entry';
import { BlogService } from 'src/app/services/blogs.service';

@Component({
    selector: 'app-blog',
    templateUrl: './blog.component.html',
    styleUrls: ['./blog.component.css']
})
export class BlogComponent implements OnInit {

    id: number;
    blog: Blog;
    entries: Array<BlogEntry>;

    constructor(private blogService: BlogService, private route: ActivatedRoute) { }

    ngOnInit(): void {
        this.route.params.subscribe(params => {
            this.id = params['id'];
            this.blogService.by_id(params['id']).subscribe(data => {
                this.blog = data;
            });
            this.blogService.entries(params['id']).subscribe(data => {
                this.entries = data;
            });
          });
    }

}
