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
    public class AngulosServices: ControllerBase
    {
        private readonly AngulosRepository _angulosRepository;

        public AngulosServices(AngulosRepository angulosRepository)
        {
            _angulosRepository = angulosRepository;
        }

        public async Task GuardarAngulo(Angulos angulos)
        {
            try
            {
                await _angulosRepository.GuardarAngulo(angulos);
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }


        public List<Angulos> GetAngulos()
        {
            try
            {
                return _angulosRepository.GetAngulos();
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
        }

        public async Task DeleteAngulos()
        {
            try
            {
                await _angulosRepository.DeleteAngulos();
            }
            catch (Exception ex)
            {
                throw new Exception(ex.Message);
            }
        }


    }
}
