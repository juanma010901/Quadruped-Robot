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
    public class ModosServices: ControllerBase
    {
        private readonly ModosRepository _modosRepository;

        public ModosServices(ModosRepository modosRepository)
        {
            _modosRepository = modosRepository;
        }

        public async Task GuardarModo(Modos modo)
        {
            try
            {
                await _modosRepository.GuardarModo(modo);
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        public async Task<IActionResult> ActualizarModo(Modos modo)
        {
            try
            {
                List<Modos> modosActual = GetModos();

                foreach (var mod in modosActual)
                {
                    if(mod.Id == modo.Id)
                    {
                        mod.Fecha = DateTime.Now;
                        mod.Activo = modo.Activo;
                    }
                    else
                    {
                        mod.Activo = false;
                    }
                }
                
                await _modosRepository.ActualizarModo(modosActual);

                return Ok(new { mensaje = "Modo actualizado con exito" });
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        public Modos GetModoActual()
        {
            try
            {
                return _modosRepository.GetModoActual();
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }


        public List<Modos> GetModos()
        {
            try
            {
                return _modosRepository.GetModos();
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }


    }
}
