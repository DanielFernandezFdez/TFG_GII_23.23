import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GuiaAnalisisComponent } from './guia-analisis.component';

describe('GuiaAnalisisComponent', () => {
  let component: GuiaAnalisisComponent;
  let fixture: ComponentFixture<GuiaAnalisisComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [GuiaAnalisisComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(GuiaAnalisisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
