using Microsoft.Azure.Functions.Extensions.DependencyInjection;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using MotionTestApi.Services;
using MotionTestApi.Repositories;

[assembly: FunctionsStartup(typeof(MotionTestApi.Startup))]
namespace MotionTestApi
{
    
    class Startup : FunctionsStartup
    {
        public override void Configure(IFunctionsHostBuilder builder)
        {

            string connectionString = Environment.GetEnvironmentVariable("SqlConnectionString");
            builder.Services.AddDbContext<EstadoContext>(
                options => SqlServerDbContextOptionsExtensions.UseSqlServer(options, connectionString));
            Console.WriteLine("");

            builder.Services.AddScoped<PuntosServices, PuntosServices>();
            builder.Services.AddScoped<ModosServices, ModosServices>();
            builder.Services.AddScoped<MovimientosServices, MovimientosServices>();
            builder.Services.AddScoped<SeccionesServices, SeccionesServices>();
            builder.Services.AddScoped<AngulosServices, AngulosServices>();



            builder.Services.AddScoped<PuntosRepository, PuntosRepository>();
            builder.Services.AddScoped<ModosRepository, ModosRepository>();
            builder.Services.AddScoped<MovimientosRepository, MovimientosRepository>();
            builder.Services.AddScoped<SeccionesRepository, SeccionesRepository>();
            builder.Services.AddScoped<AngulosRepository, AngulosRepository>();
        }
    }
}
