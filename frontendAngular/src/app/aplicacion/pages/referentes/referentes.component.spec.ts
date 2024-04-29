import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReferentesComponent } from './referentes.component';

describe('ReferentesComponent', () => {
  let component: ReferentesComponent;
  let fixture: ComponentFixture<ReferentesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ReferentesComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ReferentesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
