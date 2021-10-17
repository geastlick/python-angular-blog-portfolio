import { Component, Input, OnInit } from '@angular/core';
import { BlogEntry } from 'src/app/interfaces/blog-entry';

@Component({
  selector: 'app-entry-card',
  templateUrl: './entry-card.component.html',
  styleUrls: ['./entry-card.component.css']
})
export class EntryCardComponent implements OnInit {

    @Input() entry: BlogEntry;

  constructor() { }

  ngOnInit(): void {
  }

}
