using Microsoft.AspNetCore.Mvc;
using MotionTestApi.Models;
using MotionTestApi.Repositories;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MotionTestApi.Services
{
    public class PuntosServices: ControllerBase
    {
        private readonly PuntosRepository _puntosRepository;
        private readonly ModosServices _modosServices;

        public PuntosServices(PuntosRepository puntosRepository, ModosServices modosServices)
        {
            _puntosRepository = puntosRepository;
            _modosServices = modosServices;
        }

        public async Task GuardarPuntos(Puntos puntos)
        {
            try
            {
                await _puntosRepository.GuardarPuntos(puntos);
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        public async Task<IActionResult> ActualizarPunto(Puntos punto)
        {
            try
            {
                punto.Fecha = DateTime.Now;
                await _puntosRepository.ActualizarPunto(punto);

                Modos modo = new Modos
                {
                    Id = 8,
                    Activo = true,
                    Descripcion = "Ingreso manual de puntos",
                    SeccionId = 3,
                    Fecha = DateTime.Now
                };

                await _modosServices.ActualizarModo(modo);

                return Ok(new { mensaje = "Punto actualizado con exito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }


        public List<Puntos> GetPuntosByIds(List<int> puntos)
        {
            try
            {
                return _puntosRepository.GetPuntosByIds(puntos);
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        public List<Puntos> GetPuntosById(int puntoId)
        {
            try
            {
                return _puntosRepository.GetPuntosById(puntoId);
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }


    }
}
