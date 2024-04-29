import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DecalogoComponent } from './decalogo.component';

describe('DecalogoComponent', () => {
  let component: DecalogoComponent;
  let fixture: ComponentFixture<DecalogoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [DecalogoComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DecalogoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
