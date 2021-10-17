import { Component, OnInit } from '@angular/core';
import { Author } from 'src/app/interfaces/author';
import { AuthorService } from 'src/app/services/author.service';

@Component({
  selector: 'app-popular-authors',
  templateUrl: './popular-authors.component.html',
  styleUrls: ['./popular-authors.component.css']
})
export class PopularAuthorsComponent implements OnInit {

    popularAuthors: [Author];

  constructor(private authorService: AuthorService) { }

  ngOnInit(): void {
    this.authorService.popular()
    .subscribe(
        result => {
            this.popularAuthors = result;
        }
    );
}

}
