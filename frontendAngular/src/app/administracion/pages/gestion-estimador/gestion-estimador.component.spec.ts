import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestionEstimadorComponent } from './gestion-estimador.component';

describe('GestionEstimadorComponent', () => {
  let component: GestionEstimadorComponent;
  let fixture: ComponentFixture<GestionEstimadorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [GestionEstimadorComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(GestionEstimadorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
