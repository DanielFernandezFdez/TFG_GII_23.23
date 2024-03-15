import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CombinarAutoComponent } from './combinar-auto.component';

describe('CombinarAutoComponent', () => {
  let component: CombinarAutoComponent;
  let fixture: ComponentFixture<CombinarAutoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CombinarAutoComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CombinarAutoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
